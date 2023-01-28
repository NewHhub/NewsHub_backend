from django.urls import path
from blog.views import PostsList, LikePost

urlpatterns = [
    path('', PostsList.as_view(), name='home' ),
    path("like/", LikePost.as_view(), name='like'),
]
