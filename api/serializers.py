from rest_framework import serializers
from blog.models import Post, Tags
from users.models import User
from django.db.models import Count

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'avatar',)


class PostListSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, post):
        return post.reviews.count()

    class Meta:
        model = Post
        exclude = ('draft',)

    def get_likes_count(self, obj):
        return obj.post_by_likes.aggregate(Count('id'))['id__count']
    
    def get_comments_count(self, obj):
        return obj.post_by_review.aggregate(Count('id'))['id__count']


class PostDetailSerializer(serializers.ModelSerializer):

    tag = TagSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Post
        exclude = ('draft',)