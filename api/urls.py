from django.urls import path

from api.views import MainPageList, PostDetailView


urlpatterns = [
    path('Newsline/', MainPageList.as_view()),
    path('post/<int:pk>/', PostDetailView.as_view()),
]