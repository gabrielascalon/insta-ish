from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from .models import Post, CustomUser
from .serializers import PostSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def has_writing_permission_on_object(self, request, pk=None):
        return pk and Post.objects.get(pk=pk).user == self.request.user

    def partial_update(self, request, pk=None):
        if self.has_writing_permission_on_object(request, pk):
            return super().partial_update(request, pk)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk=None):
        if self.has_writing_permission_on_object(request, pk):
            return super().destroy(request, pk)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class CreateUserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = CustomUser.objects.none()
    serializer_class = UserSerializer
