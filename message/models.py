from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class Chat(models.Model):
    members = models.ManyToManyField(get_user_model(), verbose_name="Member", related_name="chats")
    created_at = models.DateTimeField(default=timezone.now)

    def create_message(self, user, content):
        message = Message(chat=self, user=user, content=content)
        message.save()

    def delete_message(self, message_id):
        try:
            message = self.messages.get(pk=message_id)
            message.delete()
            return True
        except Message.DoesNotExist:
            return False


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name="Chat", related_name="messages", on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), verbose_name="User", on_delete=models.CASCADE)
    content = models.TextField(max_length=300, default=True)
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['sent_at']
