from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .models import Chat, Message
from django.shortcuts import get_object_or_404
from .serializers import ChatSerializer, MessageSerializer
from rest_framework.response import Response

User = get_user_model()


class DialogsView(APIView):
    def get(self, request):
        chats = Chat.objects.filter(members__in=[request.user.id])
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)


class CreateDialogView(APIView):
    @method_decorator(login_required)
    def post(self, request):
        username = request.data.get('username')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response('User not found', status=400)

        chat = Chat.objects.create()
        chat.members.add(user)

        creator = request.user
        chat.members.add(creator)

        members = chat.members.all()
        member_ids = list(members.values_list('username', flat=True))

        data = {
            'chat_id': chat.id,
            'message': 'Chat created successfully.',
            'members': member_ids
        }
        return Response(data, status=201)


class MessagesView(APIView):
    def get_chat(self, chat_id, user):
        chat = get_object_or_404(Chat, id=chat_id)
        if user not in chat.members.all():
            chat = None
        return chat

    def post(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)
        if chat is None:
            return Response('Unauthorized', status=401)

        data = {
            'content': request.data.get('content'),
            'user': request.user.id
        }

        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save(chat=chat)
            return Response("Message sent successfully", status=201)
        return Response(serializer.errors, status=400)

