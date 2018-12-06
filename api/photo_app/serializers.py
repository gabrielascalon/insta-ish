from rest_framework import serializers
from .models import Post, CustomUser, Like, Comment, Follower
from rest_framework.authtoken.models import Token


class PostSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Post
        fields = ('id', 'user', 'image', 'description',
                  'published_date')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True},
                        'id': {'read_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['username'], validated_data['email'],
                                              validated_data['password'])
        return user


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('post.id', 'user', 'date')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'date', 'comment')


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ('following_user', 'followed_user',
                  'date')
