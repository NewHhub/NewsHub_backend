from django.urls import path
from blog.views import (
    PostsList,
    LikePost,
    TagPost,
    HotList,
    Terms,
    ExploreList,
    SearchData,
    AddPost,
    PostPage,
    AddComment,
    LikeReview,
    )

urlpatterns = [
    path('', PostsList.as_view(), name='home' ),
    path("like/", LikePost.as_view(), name='like'),
    path("like_review/", LikeReview.as_view(), name='like_review'),
    path("hot/", HotList.as_view(), name='hot'),
    path("explore/", ExploreList.as_view(), name='explore'),
    path("terms/", Terms.as_view(), name='terms'),
    path('create_post/', AddPost.as_view(), name='add_post'),
    path('add_comment', AddComment.as_view(),name='add_comment'),
    path("search/", SearchData.as_view(), name='search'),
    path('post/<int:pk>/', PostPage.as_view(), name='post_detail'),
    path("tag/<int:pk>/", TagPost.as_view(), name='tag_post'),
]
