# serializers.py
from rest_framework import serializers
from app.models import Chat, User

class StartChatSerializer(serializers.Serializer):
    name = serializers.CharField()

    def validate_name(self, value):
        try:
            recipient_user = User.objects.get(name=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("user not found")

        if not recipient_user.is_online:
            raise serializers.ValidationError("user is not online")

        return value

    def create(self, validated_data):
        current_user = self.context['request'].user
        name = validated_data['name']
        recipient_user = User.objects.get(name=name)
        chat_name = f"{current_user.name.replace(' ', '')}_{recipient_user.name.replace(' ', '')}"
        chat = Chat.objects.create(name=chat_name)
        chat.participants.add(current_user, recipient_user)

        return chat

class CreateMessageSerializer(serializers.Serializer):
    message = serializers.CharField()
