from django.contrib import admin
from .models import Chat, Message


class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'last_message_sent_at', 'all_messages']
    search_fields = ['id']
    readonly_fields = ['all_messages']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('messages')
        return qs

    def last_message_sent_at(self, obj):
        last_message = obj.messages.order_by('sent_at').first()
        return last_message.sent_at if last_message else None
    last_message_sent_at.short_description = 'Last Message Sent At'

    def all_messages(self, obj):
        messages = obj.messages.all()
        return [f'{message.user}: {message.content}' for message in messages]
    all_messages.short_description = 'All Messages'


admin.site.register(Chat, ChatAdmin)
admin.site.register(Message)
