from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from .models import Post
from django.contrib.auth.models import User
from .serializers import PostSerializer, UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CreateUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none()
    serializer_class = UserSerializer
