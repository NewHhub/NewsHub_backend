from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import PostListSerializer, PostDetailSerializer
from blog.models import Post


class PostListView(APIView):
    def get(self, request):
        posts = Post.objects.filter(draft=False)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)
    

class PostDetailView(APIView):
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        serializer = PostDetailSerializer(post, many=False)
        return Response(serializer.data)
    