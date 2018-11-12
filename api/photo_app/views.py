from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from .models import Post, CustomUser
from .serializers import PostSerializer, UserSerializer
from rest_framework.permissions import AllowAny


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CreateUserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = CustomUser.objects.none()
    serializer_class = UserSerializer
