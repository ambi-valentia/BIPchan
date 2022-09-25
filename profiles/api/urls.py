from django.urls import path

from .views import (
    profile_detail_api_view,
    profile_update_api_view
)

# /api/profiles/
urlpatterns = [
    path('<str:username>/', profile_detail_api_view),
    path('', profile_update_api_view),
]
