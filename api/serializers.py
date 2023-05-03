from rest_framework import serializers
from blog.models import Post, Tags
from users.models import User


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'text')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'avatar',)


class PostDetailSerializer(serializers.ModelSerializer):

    tag = TagSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Post
        exclude = ('draft',)