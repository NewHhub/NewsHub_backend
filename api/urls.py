from django.urls import path

from api.views import PostListView, PostDetailView


urlpatterns = [
    path('post_list/', PostListView.as_view()),
    path('post/<int:pk>/', PostDetailView.as_view()),
]