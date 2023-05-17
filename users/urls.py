from django.urls import path, include
from users.views import Register, Follow, Unfollow, profile_settings, CustomPasswordResetView

urlpatterns = [
    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path('register/', Register.as_view(), name='register'),
    path('follow/', Follow.as_view(), name='follow'),
    path('unfollow/', Unfollow.as_view(), name='unfollow'),
    path('profile-settings/', profile_settings, name='profile_settings'),
    path('', include('django.contrib.auth.urls')),
]
