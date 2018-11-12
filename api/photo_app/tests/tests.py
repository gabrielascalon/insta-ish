from django.test import TestCase
import json
from django.core.files.base import ContentFile
from .factories import PostFactory, UserFactory
from django.urls import reverse
from photo_app.models import Post, CustomUser
from rest_framework.authtoken.models import Token


class PostTestCase(TestCase):

    def setUp(self):
        self.image = ContentFile(
            b"GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x00;", name='image.gif')
        self.description = 'This is a test post for my Post tests'
        self.user = UserFactory()
        self.header = {
            'HTTP_AUTHORIZATION': 'Token {}'.format(self.user.auth_token.key)}

    def test_get_all_posts(self):
        PostFactory.create_batch(2)
        response = self.client.get('/posts/', **self.header)
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json), 2)

    def test_get_post(self):
        post = PostFactory()
        url = '/posts/{}/'.format(post.pk)
        response = self.client.get(url, **self.header)
        response_json = response.json()
        self.assertIn(post.image.url, response_json['image'])
        self.assertEqual(post.description, response_json['description'])
        self.assertEqual(post.published_date.isoformat()[:-6] + 'Z',
                         response_json['published_date'])

    def test_create_new_post(self):
        data = {'image': self.image, 'description': self.description}
        response = self.client.post(
            '/posts/', data, format='multipart', **self.header)
        self.assertEqual(response.status_code, 201)

    def test_no_description(self):
        data = {'image': self.image}
        response = self.client.post(
            '/posts/', data, format='multipart', **self.header)
        self.assertEqual(response.status_code, 201)

    def test_no_image(self):
        data = {'description': self.description}
        response = self.client.post(
            '/posts/', data, format='multipart', **self.header)
        self.assertEqual(response.status_code, 400)

    def test_delete_post(self):
        post = PostFactory()
        pk = post.pk
        url = '/posts/{}/'.format(pk)
        response = self.client.delete(url, **self.header)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Post.objects.filter(pk=pk).exists())

    def test_edit_post(self):
        post = PostFactory()
        pk = post.pk
        url = '/posts/{}/'.format(pk)
        data = json.dumps({'description': self.description})
        response = self.client.patch(
            url, data, content_type='application/json', **self.header)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.description in str(response.content))

    def edit_published_date(self):
        post = PostFactory()
        pk = post.pk
        post_published_date = post.published_date
        url = '/posts/{}/'.format(pk)
        data = json.dumps({'published_date': '1995-11-02T10:49:03.916596Z'})
        response = self.client.patch(
            url, data, content_type='application/json', **self.header)
        post = post.refresh_from_db()
        self.assertEqual(post.published_date, post_published_date)


class UserTestCase(TestCase):
    def test_create_new_user(self):
        data = {'username': 'test_username',
                'email': 'test@test.com', 'password': 'test123'}
        self.client.post('/users/', data, format='application/json')
        self.assertTrue(CustomUser.objects.filter(
            username=data['username']).exists())
        user = CustomUser.objects.get(username=data['username'])
        self.assertTrue(Token.objects.filter(user=user).exists())

    def test_update_user(self):
        user = UserFactory()
        user_id = user.pk
        new_username = 'test username'
        user = CustomUser.objects.get(id=user.pk)
        user.username = new_username
        user.save()
        user.refresh_from_db()
        self.assertEqual(new_username, user.username)

    def test_login_valid_credentials(self):
        password = 'validpass'
        user = UserFactory(password=password)
        response = self.client.post(
            '/api-token-auth/', {'username': user.username, 'password': password})
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.auth_token.key, response_json['token'])

    def test_login_invalid_credentials(self):
        password = 'validpass'
        user = UserFactory(password=password)
        response = self.client.post(
            '/api-token-auth/', {'username': user.username, 'password': 'invalidpass'})
        response_json = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertFalse(user.auth_token.key in response_json)
