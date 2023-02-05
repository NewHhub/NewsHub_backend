from django.urls import path
from blog.views import PostsList, LikePost, TagPost

urlpatterns = [
    path('', PostsList.as_view(), name='home' ),
    path("like/", LikePost.as_view(), name='like'),
    path("tag/<slug:slug>/", TagPost.as_view(), name='tag_post'),
]
