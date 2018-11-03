from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('image', 'description', 'published_date')

    def validate(self, data):
        print('*' * 80)
        print(data)
        print('*' * 80)
        return data
