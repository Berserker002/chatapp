from django.urls import path
from .consumers import SendMessageConsumer

websocket_urlpatterns = [
    path('api/chat/send/<str:room_name>', SendMessageConsumer.as_asgi()),
]