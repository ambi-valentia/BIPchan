from django.http import request
from rest_framework import serializers

from .models import Profile

class PublicProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    follower_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "id",
            "bio",
            "follower_count",
            "following_count",
            "is_following",
            "username",
        ]
    
    def get_is_following(self, obj):
        # request???
        is_following = False
        context = self.context
        request = context.get("request")
        if request:
            user = request.user
            is_following = user in obj.followers.all()
        return is_following
    
    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name
    
    def get_username(self, obj):
        return obj.user.username
    
    def get_following_count(self, obj):
        return obj.user.following.count()
    
    def get_follower_count(self, obj):
        return obj.followers.count()

class ProfileEditSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source = 'user.first_name',  allow_blank=True, allow_null=True, required=False)
    last_name = serializers.CharField(source = 'user.last_name', allow_blank=True, allow_null=True, required=False)
    username = serializers.CharField(source = 'user.username', read_only = True, required=False)
    email = serializers.CharField(source = 'user.email', allow_blank=True, allow_null=True, required=False)
    class Meta:
        model = Profile
        fields = [
            #"id",
            "username",
            "first_name",
            "last_name",
            "bio",
            "email",
            "telegram_id"
        ]

    def update(self, instance, validated_data):
        user = instance.user     
        user_data = validated_data.get('user', None)
        if user_data:
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name )
            user.email = user_data.get('email', user.email)
        user.save()
        instance.bio = validated_data.get('bio', instance.bio)
        instance.telegram_id = validated_data.get('telegram_id', instance.telegram_id )
        instance.save()
        return instance