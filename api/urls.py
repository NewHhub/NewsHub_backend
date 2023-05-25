from django.urls import path

from api.views import MainPageList, PostDetailView, HotFeedsList, ExploreFeedsList, ReviewsCreateView


urlpatterns = [
    path('Newsline/', MainPageList.as_view()),
    path('Hot_feeds/', HotFeedsList.as_view()),
    path('Explore/', ExploreFeedsList.as_view()),
    path('post/<int:pk>/', PostDetailView.as_view()),
    path('reviews/create/', ReviewsCreateView.as_view()),
]