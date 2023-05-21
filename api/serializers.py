from collections import OrderedDict
from rest_framework import serializers
from blog.models import Post, Tags, Reviews
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
    liked_by_user = serializers.SerializerMethodField()

    def get_comments_count(self, post):
        return post.post_by_review.aggregate(Count('id'))['id__count']

    def get_likes_count(self, obj):
        return obj.post_by_likes.aggregate(Count('id'))['id__count']
    
    def get_liked_by_user(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.post_by_likes.filter(user__id=user.id).exists()
        return False

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['liked_by_user'] = self.get_liked_by_user(instance)
        return representation

    class Meta:
        model = Post
        exclude = ('draft',)


class ReviewSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    liked_by_user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.review_for_likes.aggregate(Count('id'))['id__count']

    def get_liked_by_user(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.review_for_likes.filter(user__id=user.id).exists()
        return False
    

    class Meta:
        model = Reviews
        exclude = ('post',)


class OrderedSerializer(serializers.Serializer):
    def get_fields(self):
        fields = super().get_fields()
        ordered_fields = OrderedDict()

        field_order = ['id', 'title', 'text', 'poster', 'date', 'tag', 'owner', 'review']

        for field_name in field_order:
            if field_name in fields:
                ordered_fields[field_name] = fields[field_name]

        return ordered_fields


class PostDetailSerializer(OrderedSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    text = serializers.CharField()
    poster = serializers.CharField()
    date = serializers.DateTimeField()
    tag = TagSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    review = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        exclude = ('draft',)