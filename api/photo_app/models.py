from django.db import models
from django.utils import timezone


class Post(models.Model):
    # user = models.ForeignKey('auth.User', models.on_delete=CASCADE)
    image = models.ImageField(upload_to='static/photos/')
    description = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
