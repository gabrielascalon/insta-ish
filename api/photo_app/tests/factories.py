import factory
from photo_app.models import Post, CustomUser
from rest_framework.authtoken.models import Token


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
    username = factory.Sequence(lambda n: "User {0}".format(n))
    email = factory.Sequence(lambda n: 'user{0}@test.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'validpass')


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
    user = factory.SubFactory(UserFactory)
    image = factory.django.ImageField()
    description = 'Hello, this is a description'
