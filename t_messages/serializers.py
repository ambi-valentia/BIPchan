from django.conf import settings
from rest_framework import serializers
from profiles.serializers import PublicProfileSerializer
from .models import Message
from threads.models import Thread

MAX_MESSAGE_LENGTH = settings.MAX_MESSAGE_LENGTH
MAX_THREAD_LENGTH = settings.MAX_THREAD_LENGTH
MESSAGE_ACTION_OPTIONS = settings.MESSAGE_ACTION_OPTIONS

class MessageActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in MESSAGE_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for message")
        return value

class MessageCreateSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source='user.profile', read_only=True) 
    likes = serializers.SerializerMethodField(read_only=True)
    thread = serializers.CharField()
    class Meta:
        model = Message
        fields = ['id', 'content', 'thread', 'image', 'likes', "user"]

    def get_likes(self, obj):
        return obj.likes.count()
    
    def validate_thread(self, value):
        if len(value) > MAX_THREAD_LENGTH:
            raise serializers.ValidationError("This thread name is too long")
        value = value.lower()
        return value

    def validate_content(self, value):
        if len(value) > MAX_MESSAGE_LENGTH:
            raise serializers.ValidationError("This message is too long")
        return value

    def create(self, validated_data):
        thread_data = validated_data.pop('thread')
        thread = Thread.objects.filter(name=thread_data).first()
        if not thread: 
            thread = Thread.objects.create(name=thread_data)
        return Message.objects.create(thread=thread, **validated_data)
        
class MessageSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source='user.profile', read_only=True) 
    likes = serializers.SerializerMethodField(read_only=True)
    thread = serializers.SerializerMethodField(read_only=True)
    image = serializers.ImageField()
    class Meta:
        model = Message
        fields = ['id', 'content', 'thread', 'image', 'likes', "user"]
    
    def get_thread(self, obj):
        return obj.thread.name

    def get_likes(self, obj):
        return obj.likes.count()
