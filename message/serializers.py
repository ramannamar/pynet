from rest_framework import serializers
from .models import Chat, Message
from django.contrib.auth import get_user_model


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), label="User", write_only=True)

    class Meta:
        model = Message
        fields = ['id', 'user', 'content', 'sent_at']


class ChatSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), many=True, label="Member")
    message = MessageSerializer(write_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'members', 'created_at', 'message']

    def create(self, validated_data):
        members = validated_data.pop('members')
        message_data = validated_data.pop('message')
        chat = Chat.objects.create(**validated_data)
        chat.members.set(members)

        message_serializer = MessageSerializer(data=message_data)
        if message_serializer.is_valid():
            message_serializer.save(chat=chat, author=self.context['request'].user)
        else:

            raise serializers.ValidationError(message_serializer.errors)

        return chat
