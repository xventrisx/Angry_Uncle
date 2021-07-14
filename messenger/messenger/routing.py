from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/web/chat_with_user/<int:id>/', consumers.ChatConsumer.as_asgi()),
]
