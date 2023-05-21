from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import PostListSerializer, PostDetailSerializer, ReviewSerializer
from blog.models import Post
from django.contrib.auth.models import AnonymousUser
from django.db.models import Count


class PostListView(APIView):
    anonimys = AnonymousUser()

    def get_data(self, request):
        posts = Post.objects.filter(draft=False)
        serializer = PostListSerializer(posts, many=True)
        return serializer

    def get(self, request):
        serializer = self.get_data(request)
        return Response(serializer.data)
    

class MainPageList(PostListView):

    def get_data(self, request):
        if self.request.user!=self.anonimys:
            following_users = [f.follow_by for f in self.request.user.following.all()]
        else:
            following_users = None

        # в запросе мы не встретим посты если мы авторизированы и при этом не подписаны не на кого
        if self.request.user!=self.anonimys and following_users:
            # если человек авторизирован, то нужно выводить только тех на кого он подписан (себя выводить не стоит)
            post_queryset = Post.objects.filter(owner__in=following_users, draft=False).order_by('-date')
        elif self.request.user!=self.anonimys and not following_users:
            # ненужно делать запрос на посты если мы не на кого не подписаны
            post_queryset = list()
        else:
            # если человек аноним, выводим все посты всех пользователей (кторые активные)
            post_queryset = Post.objects.filter(draft=False).order_by('-date')

        serializer = PostListSerializer(post_queryset, many=True, context={'request': request})
        return serializer


class HotFeedsList(PostListView):
    def get_data(self, request):
        post_queryset = Post.objects.annotate(num_likes=Count('post_by_likes')).filter(draft=False).order_by('-num_likes', '-date')
        serializer = PostListSerializer(post_queryset, many=True, context={'request': request})
        return serializer


class ExploreFeedsList(PostListView):
    def get_data(self, request):
        post_queryset = Post.objects.filter(draft=False).order_by('-date')
        serializer = PostListSerializer(post_queryset, many=True, context={'request': request})
        return serializer


class PostDetailView(APIView):
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        serializer = PostDetailSerializer(post, many=False)
        comments = post.post_by_review.all()  # Получение всех комментариев для данного поста
        comments_serializer = ReviewSerializer(comments, many=True, context={'request': request})  # Подставьте соответствующий сериализатор комментария
        data = serializer.data
        data['review'] = comments_serializer.data  # Добавление данных комментариев в сериализованный результат

        return Response(data)
    