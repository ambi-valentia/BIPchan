from django.urls import path

from .views import (
    thread_view
)

urlpatterns = [
    path('<str:thread>/', thread_view)
]