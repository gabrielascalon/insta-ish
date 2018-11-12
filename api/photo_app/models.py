from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    # user = models.ForeignKey('auth.User', models.on_delete=CASCADE)
    image = models.ImageField(upload_to='static/photos/')
    description = models.TextField(blank=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
