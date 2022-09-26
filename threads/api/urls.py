from django.urls import path

from .views import (
    thread_action_view,
    thread_detail_view
)

urlpatterns = [
    path('action/', thread_action_view),
    path('<str:thread>/', thread_detail_view),
]
