from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


class Post(models.Model):
    # user = models.ForeignKey('auth.User', models.on_delete=CASCADE)
    image = models.ImageField(upload_to='static/photos/')
    description = models.TextField(blank=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class CustomUser(AbstractUser):

    def save(self, *args, **kwargs):
        creating = not self.pk
        instance = super().save(*args, **kwargs)
        if creating:
            Token.objects.create(user_id=self.pk)
        return instance
