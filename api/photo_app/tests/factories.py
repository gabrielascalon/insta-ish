import factory
from photo_app.models import Post


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
    image = factory.django.ImageField()
    description = 'Hello, this is a description'
