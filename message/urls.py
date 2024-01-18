from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.DialogsView.as_view(), name='messages'),
    path('create/', views.CreateDialogView.as_view(), name='create_dialog'),
    path('<int:chat_id>/', views.MessagesView.as_view(), name='view_messages'),
    path('<int:chat_id>/', views.SendMessageView.as_view(), name='send_message'),
    path('<int:chat_id>/messages/<int:message_id>/delete/', views.DeleteMessageView.as_view(), name='delete_message'),
]
