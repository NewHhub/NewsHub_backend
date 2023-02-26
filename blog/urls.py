from django.urls import path
from blog.views import PostsList, LikePost, TagPost, HotList

urlpatterns = [
    path('', PostsList.as_view(), name='home' ),
    path("like/", LikePost.as_view(), name='like'),
    path("hot/", HotList.as_view(), name='hot'),
    path("tag/<slug:slug>/", TagPost.as_view(), name='tag_post'),
]
