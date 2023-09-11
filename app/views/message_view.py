# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from app.models import Chat, User
from app.serializers.message import StartChatSerializer, CreateMessageSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class StartChatAPIView(generics.CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = StartChatSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        chat = serializer.save()

        return Response({'message': 'Chat started successfully', 'chat_id': chat.id, 'chat_name': chat.name}, status=status.HTTP_201_CREATED)
