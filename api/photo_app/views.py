from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from .models import Post, CustomUser, Like, Comment
from .serializers import PostSerializer, UserSerializer, LikeSerializer, CommentSerializer
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


class LikeViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk, post_id=None):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['post_id'])
        serializer_data = Like.objects.get(pk=pk)
        serializer = LikeSerializer(serializer_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, post_id=None):
        post = Post.objects.get(pk=self.kwargs['post_id'])
        if Like.objects.filter(user=self.request.user, post=post):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            Like.objects.create(user=self.request.user, post=post)
            return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, pk, post_id=None):
        like = Like.objects.get(pk=pk)
        if like.user == self.request.user:
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class CommentViewset(viewsets.ViewSet):

    def retrieve(self, request, pk, post_id=None):
        user = self.request.user
        post = Post.objects.get(pk=post_id)
        serializer_data = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(serializer_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, post_id=None):
        post = Post.objects.get(pk=self.kwargs['post_id'])
        serializer_data = Comment.objects.create(
            user=self.request.user, post=post)
        serializer = CommentSerializer(serializer_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk, post_id=None):
        comment = Comment.objects.get(pk=pk)
        if comment.user == self.request.user:
            serializer = CommentSerializer(
                comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk, post_id=None):
        comment = Comment.objects.get(pk=pk)
        if comment.user == self.request.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class CreateUserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = CustomUser.objects.none()
    serializer_class = UserSerializer
