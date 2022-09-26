from django.conf import settings
from rest_framework import serializers
from profiles.serializers import PublicProfileSerializer
from .models import Thread
from t_messages.models import Message

MAX_THREAD_LENGTH = settings.MAX_THREAD_LENGTH
THREAD_ACTION_OPTIONS = settings.THREAD_ACTION_OPTIONS

class ThreadActionSerializer(serializers.Serializer):
    thread_name = serializers.CharField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in THREAD_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for threads")
        return value

class ThreadSerializer(serializers.ModelSerializer):
    subscribers_count = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Thread
        fields = [
            "name",
            "subscribers_count",
            "is_subscribed",
            ]

    def get_subscribers_count(self, obj):
        return obj.subscribers.count()

    def get_is_subscribed(self, obj):
        # request???
        is_subscribed = False
        context = self.context
        request = context.get("request")
        if request:
            user = request.user.profile
            is_subscribed = user in obj.subscribers.all()
        return is_subscribed