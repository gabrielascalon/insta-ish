from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


class Post(models.Model):
    user = models.ForeignKey('photo_app.CustomUser',
                             on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/photos/')
    description = models.TextField(blank=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Like(models.Model):
    user = models.ForeignKey('photo_app.CustomUser', on_delete=models.CASCADE)
    post = models.ForeignKey('photo_app.Post', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} liked post {}'.format(user.username, post.id)


class Comment(models.Model):
    user = models.ForeignKey('photo_app.CustomUser', on_delete=models.CASCADE)
    post = models.ForeignKey('photo_app.Post', on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} commented on post {}'.format(user.username, post.id)


class Follower(models.Model):
    class Meta:
        unique_together = ("following_user", "followed_user")

    following_user = models.ForeignKey('photo_app.CustomUser',
                                       on_delete=models.CASCADE, related_name='following_user')
    followed_user = models.ForeignKey(
        'photo_app.CustomUser', on_delete=models.CASCADE, related_name='followed_user')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} started to follow {}'.format(user, followed_user)


class CustomUser(AbstractUser):

    def save(self, *args, **kwargs):
        creating = not self.pk
        instance = super().save(*args, **kwargs)
        if creating:
            Token.objects.create(user_id=self.pk)
        return instance
