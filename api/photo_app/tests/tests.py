from django.test import TestCase
import json
from django.core.files.base import ContentFile
from .factories import PostFactory, UserFactory, CommentFactory, LikeFactory, FollowerFactory
from django.urls import reverse
from photo_app.models import Post, CustomUser, Like, Comment, Follower
from rest_framework.authtoken.models import Token


class PostTestCase(TestCase):

    def setUp(self):
        self.image = ContentFile(
            b"GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x00;", name='image.gif')
        self.description = 'This is a test post for my Post tests'
        self.user = UserFactory()
        self.auth = {
            'HTTP_AUTHORIZATION': 'Token {}'.format(self.user.auth_token.key)}

    def test_get_all_posts(self):
        PostFactory.create_batch(2)
        response = self.client.get('/posts/', **self.auth)
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json), 2)

    def test_get_post(self):
        post = PostFactory()
        url = '/posts/{}/'.format(post.pk)
        response = self.client.get(url, **self.auth)
        response_json = response.json()
        self.assertIn(post.image.url, response_json['image'])
        self.assertEqual(post.description, response_json['description'])
        self.assertEqual(post.published_date.isoformat()[:-6] + 'Z',
                         response_json['published_date'])

    def test_create_new_post(self):
        data = {'image': self.image, 'description': self.description}
        response = self.client.post(
            '/posts/', data, format='multipart', **self.auth)
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        response_id = response_json['id']
        post = Post.objects.get(id=response_id)
        self.assertEqual(self.user.username, post.user.username)

    def test_no_description(self):
        data = {'image': self.image}
        response = self.client.post(
            '/posts/', data, format='multipart', **self.auth)
        self.assertEqual(response.status_code, 201)

    def test_no_image(self):
        data = {'description': self.description}
        response = self.client.post(
            '/posts/', data, format='multipart', **self.auth)
        self.assertEqual(response.status_code, 400)

    def test_delete_post(self):
        post = PostFactory(user=self.user)
        pk = post.pk
        url = '/posts/{}/'.format(pk)
        response = self.client.delete(url, **self.auth)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Post.objects.filter(pk=pk).exists())

    def test_delete_post_other_user(self):
        post = PostFactory(user=self.user)
        other_user = UserFactory()
        other_user_auth = {
            'HTTP_AUTHORIZATION': 'Token {}'.format(other_user.auth_token.key)}
        pk = post.pk
        url = '/posts/{}/'.format(pk)
        response = self.client.delete(url, **other_user_auth)
        self.assertEqual(response.status_code, 401)
        self.assertTrue(Post.objects.filter(pk=pk).exists())

    def test_edit_post(self):
        post = PostFactory(user=self.user)
        pk = post.pk
        url = '/posts/{}/'.format(pk)
        data = json.dumps({'description': self.description})
        response = self.client.patch(
            url, data, content_type='application/json', **self.auth)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.description in str(response.content))

    def test_edit_post_other_user(self):
        post = PostFactory()
        pk = post.pk
        other_user = UserFactory()
        other_user_auth = {
            'HTTP_AUTHORIZATION': 'Token {}'.format(other_user.auth_token.key)}
        url = '/posts/{}/'.format(pk)
        data = json.dumps({'description': self.description})
        response = self.client.patch(
            url, data, content_type='application/json', **other_user_auth)
        self.assertFalse(self.description in str(response.content))
        self.assertFalse(post.user == other_user)
        self.assertEqual(response.status_code, 401)

    def edit_published_date(self):
        post = PostFactory(user=self.user)
        pk = post.pk
        post_published_date = post.published_date
        url = '/posts/{}/'.format(pk)
        data = json.dumps({'published_date': '1995-11-02T10:49:03.916596Z'})
        response = self.client.patch(
            url, data, content_type='application/json', **self.auth)
        post = post.refresh_from_db()
        self.assertEqual(post.published_date, post_published_date)

    def test_substitute_post(self):
        post = PostFactory(user=self.user)
        pk = post.pk
        url = '/posts/{}/'.format(pk)
        data = json.dumps({'description': self.description})
        response = self.client.put(
            url, data, content_type='application/json', **self.auth)
        self.assertEqual(response.status_code, 405)


class LikeTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.auth = {'HTTP_AUTHORIZATION': 'Token {}'.format(
            self.user.auth_token.key)}
        self.post = PostFactory()

    def test_like_post(self):
        url = '/posts/{}/likes/'.format(self.post.pk)
        response = self.client.post(url, **self.auth)
        self.assertTrue(Like.objects.filter(
            user=self.user, post=self.post).exists())
        self.assertEqual(response.status_code, 201)

    def test_user_like_post_twice(self):
        Like.objects.create(user=self.user, post=self.post)
        url = '/posts/{}/likes/'.format(self.post.pk)
        response = self.client.post(url, **self.auth)
        self.assertTrue(Like.objects.filter(
            user=self.user, post=self.post).count() == 1)
        self.assertEqual(response.status_code, 400)

    def test_delete_like(self):
        like = LikeFactory(user=self.user, post=self.post)
        url = '/posts/{}/likes/{}/'.format(self.post.pk, like.pk)
        response = self.client.delete(url, **self.auth)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Like.objects.filter(pk=like.pk).exists())

    def test_delete_like_other_user(self):
        like = LikeFactory(user=self.user, post=self.post)
        other_user = UserFactory()
        other_user_auth = {
            'HTTP_AUTHORIZATION': 'Token {}'.format(other_user.auth_token.key)}
        url = '/posts/{}/likes/{}/'.format(self.post.pk, like.pk)
        response = self.client.delete(url, **other_user_auth)
        self.assertEqual(response.status_code, 401)
        self.assertTrue(Like.objects.filter(pk=like.pk).exists())


class CommentTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.auth = {'HTTP_AUTHORIZATION': 'Token {}'.format(
            self.user.auth_token.key)}
        self.post = PostFactory()

    def test_comment_on_post(self):
        url = '/posts/{}/comments/'.format(self.post.pk)
        response = self.client.post(url, **self.auth)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Comment.objects.filter(
            user=self.user, post=self.post).exists())

    def test_delete_comment(self):
        comment = CommentFactory(user=self.user, post=self.post)
        url = '/posts/{}/comments/{}/'.format(self.post.pk, comment.pk)
        response = self.client.delete(url, **self.auth)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())

    def test_delete_comment_other_user(self):
        comment = CommentFactory(post=self.post)
        other_user = UserFactory()
        other_user_auth = {
            'HTTP_AUTHORIZATION': 'Token {}'.format(other_user.auth_token.key)}
        url = '/posts/{}/comments/{}/'.format(self.post.pk, comment.pk)
        response = self.client.delete(url, **other_user_auth)
        self.assertEqual(response.status_code, 401)
        self.assertTrue(Comment.objects.filter(pk=comment.pk).exists())

    def test_partial_update_comment(self):
        comment = CommentFactory(user=self.user, post=self.post)
        url = '/posts/{}/comments/{}/'.format(self.post.pk, comment.pk)
        data = {'comment': 'Hello, this is the new test description'}
        response = self.client.patch(
            url, data, content_type='application/json', **self.auth)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['comment'] in str(response.data))
        self.assertEqual(Comment.objects.get(
            pk=comment.pk).comment, data['comment'])


class FollowerTestCase(TestCase):
    def setUp(self):
        self.followed_user = UserFactory()
        self.following_user = UserFactory()
        self.auth = {'HTTP_AUTHORIZATION': 'Token {}'.format(
            self.following_user.auth_token.key)}

    def test_follow_user(self):
        url = '/users/{}/followers/'.format(self.followed_user.pk)
        response = self.client.post(url, **self.auth)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Follower.objects.filter(
            followed_user=self.followed_user, following_user=self.following_user).exists())

    def test_follow_user_twice(self):
        FollowerFactory(followed_user=self.followed_user,
                        following_user=self.following_user)
        url = '/users/{}/followers/'.format(self.followed_user.pk)
        response = self.client.post(url, **self.auth)
        self.assertTrue(Follower.objects.filter(
            followed_user=self.followed_user, following_user=self.following_user).count() == 1)
        self.assertEqual(response.status_code, 400)

    def test_delete_follow(self):
        follow = FollowerFactory(
            followed_user=self.followed_user, following_user=self.following_user)
        url = '/users/{}/followers/{}/'.format(
            self.followed_user.pk, follow.pk)
        response = self.client.delete(url, **self.auth)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Follower.objects.filter(pk=follow.pk).exists())

    def test_delete_follow_other_user(self):
        follow = FollowerFactory(
            followed_user=self.followed_user, following_user=self.following_user)
        other_user = UserFactory()
        other_user_auth = {
            'HTTP_AUTHORIZATION': 'Token {}'.format(other_user.auth_token.key)}
        url = '/users/{}/followers/{}/'.format(
            self.followed_user.pk, follow.pk)
        response = self.client.delete(url, **other_user_auth)
        self.assertEqual(response.status_code, 401)
        self.assertTrue(Follower.objects.filter(pk=follow.pk).exists())


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
