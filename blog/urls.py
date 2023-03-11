from django.urls import path
from blog.views import (
    PostsList,
    LikePost,
    TagPost,
    HotList,
    Terms,
    ExploreList,
    SearchData,
    AddPost
    )

urlpatterns = [
    path('', PostsList.as_view(), name='home' ),
    path("like/", LikePost.as_view(), name='like'),
    path("hot/", HotList.as_view(), name='hot'),
    path("explore/", ExploreList.as_view(), name='explore'),
    path("terms/", Terms.as_view(), name='terms'),
    path('create_post/', AddPost.as_view(), name='add_post'),
    path("search/", SearchData.as_view(), name='search'),
    path("tag/<slug:slug>/", TagPost.as_view(), name='tag_post'),
]
