"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from photo_app import views
from rest_framework.authtoken.views import obtain_auth_token


router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'users', views.CreateUserViewSet)
router.register(r'posts/(?P<post_id>\d+)/likes',
                views.LikeViewSet, basename='likes')
router.register(r'posts/(?P<post_id>\d+)/comments',
                views.CommentViewset, basename='comments')
router.register(r'users/(?P<followed_user_id>\d+)/followers',
                views.FollowerViewSet, basename='followers')


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', obtain_auth_token), ]
