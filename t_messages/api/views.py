import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Message
from profiles.models import Profile
from threads.models import Thread
from telegrambot.views import TelegramBot
from ..serializers import (
    MessageSerializer, 
    MessageActionSerializer,
    MessageCreateSerializer
)

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def message_action_view(request, *args, **kwargs):
    serializer = MessageActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        message_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Message.objects.filter(id=message_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = MessageSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = MessageSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "delete":
            obj = obj.filter(user=request.user)
            if not obj.exists():
                return Response({"message": "You cannot delete this message"}, status=401)
            obj = obj.first()
            obj.delete()
            return Response({"message": "Message removed"}, status=200)
    return Response({}, status=200)

@api_view(['POST']) 
@permission_classes([IsAuthenticated]) # REST API course
def message_create_view(request, *args, **kwargs):
    serializer = MessageCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        message = serializer.save(user=request.user)
        for profile in Profile.objects.filter(Q(subscriptions = message.thread) | Q(user__following = message.user.profile)).distinct():
            if(profile.telegram_id):
                TelegramBot.send_notification("127.0.0.1:8000/feed/", profile.telegram_id)
        return Response(MessageSerializer(message).data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def message_detail_view(request, message_id, *args, **kwargs):
    qs = Message.objects.filter(id=message_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = MessageSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def message_list_view(request, *args, **kwargs):
    qs = Message.objects.all()
    search = request.GET.get("search", None)
    if search:  
        qs = qs.filter(Q(user__username__icontains = search)|Q(thread__name__icontains = search)|Q(content__icontains = search))
    else:
        user = request.GET.get("user", None)
        if user:  
            #uqs = User.objects.filter(username = user).first()
            qs = qs.filter(user__username__iexact = user)
        thread = request.GET.get("thread", None)
        if thread: 
            #tqs = Thread.objects.filter(name = thread).first()
            qs = qs.filter(thread__name__iexact = thread)
    serializer = MessageSerializer(qs, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def message_feed_view(request, *args, **kwargs):
    user = request.user
    qs = Message.objects.feed(user)
    serializer = MessageSerializer(qs, many=True)
    return Response(serializer.data, status=200)