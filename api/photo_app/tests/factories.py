import factory
from photo_app.models import Post
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
    image = factory.django.ImageField()
    description = 'Hello, this is a description'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: "User {0}".format(n))
    email = factory.Sequence(lambda n: 'user{0}@test.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'validpass')
