from django.urls import path

from .views import (
    message_action_view,
    message_detail_view,
    message_feed_view,
    message_list_view,
    message_create_view
)
'''
CLIENT
Base ENDPOINT /api/messages/
'''
urlpatterns = [
    path('', message_list_view),
    path('feed/', message_feed_view),
    path('action/', message_action_view),
    path('create/', message_create_view),
    path('<int:message_id>/', message_detail_view),
]