from rest_framework import serializers
from .models import Post, CustomUser
from rest_framework.authtoken.models import Token


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('image', 'description', 'published_date')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['username'], validated_data['email'],
                                              validated_data['password'])
        return user
