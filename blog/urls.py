from django.urls import path
from blog.views import PostsList, LikePost, TagPost, HotList, Terms

urlpatterns = [
    path('', PostsList.as_view(), name='home' ),
    path("like/", LikePost.as_view(), name='like'),
    path("hot/", HotList.as_view(), name='hot'),
    path("terms/", Terms.as_view(), name='terms'),
    path("tag/<slug:slug>/", TagPost.as_view(), name='tag_post'),
]
