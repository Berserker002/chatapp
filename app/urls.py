from django.urls import path
from app.views.user_view import UserRegistrationView, UserLoginView, OnlineUserListView, RecommendedListView
from app.views.message_view import StartChatAPIView
from .consumers import SendMessageConsumer

urlpatterns = [
    path('register', UserRegistrationView.as_view(), name='user-registration'),
    path('login', UserLoginView.as_view(), name='user-login'),
    path('online-users', OnlineUserListView.as_view(), name='online-users'),
    path('start-chat', StartChatAPIView.as_view(), name='start-chat'),
    path('suggested-friends/<str:user_id>',RecommendedListView.as_view(), name='suggested-freinds')
]


