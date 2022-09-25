from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Thread
from ..serializers import (
    ThreadActionSerializer,
    ThreadSerializer
)

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def thread_action_view(request, *args, **kwargs):
    serializer = ThreadActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        thread_name = data.get("thread_name")
        action = data.get("action")
        content = data.get("content")
        qs = Thread.objects.filter(name=thread_name)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        me = request.user.profile
        if action == "subscribe":
            obj.subscribers.add(me)
            return Response(ThreadSerializer(instance=obj, context={"request": request}).data, status=200)
        elif action == "unsubscribe":
            obj.subscribers.remove(me)
            return Response(ThreadSerializer(instance=obj, context={"request": request}).data, status=200)
    return Response({}, status=200)

@api_view(['GET'])
def thread_detail_view(request, thread, *args, **kwargs):
    qs = Thread.objects.filter(name=thread)
    if not qs.exists():
        return Response({"detail": "Thread not found"}, status=404)
    thread_obj = qs.first()
    return Response(ThreadSerializer(instance=thread_obj, context={"request": request}).data, status=200)