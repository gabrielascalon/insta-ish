import factory
from photo_app.models import Post, CustomUser
from rest_framework.authtoken.models import Token


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
    image = factory.django.ImageField()
    description = 'Hello, this is a description'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
    username = factory.Sequence(lambda n: "User {0}".format(n))
    email = factory.Sequence(lambda n: 'user{0}@teste.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'validpass')
