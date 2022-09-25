from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Profile
from ..serializers import PublicProfileSerializer, ProfileEditSerializer
from ..forms import ProfileForm

@api_view(['GET', 'POST'])
def profile_detail_api_view(request, username, *args, **kwargs):
    # get the profile for the passed username
    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        return Response({"detail": "User not found"}, status=404)
    profile_obj = qs.first()
    data = request.data or {}
    if request.method == "POST":
        print(data)
        me = request.user
        action = data.get("action")
        if profile_obj.user != me:
            if action == "follow":
                profile_obj.followers.add(me)
            elif action == "unfollow":
                profile_obj.followers.remove(me)
            else:
                pass
    serializer = PublicProfileSerializer(instance=profile_obj, context={"request": request})
    return Response(serializer.data, status=200)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def profile_update_api_view(request, *args, **kwargs):
    qs = Profile.objects.filter(user=request.user)
    profile_obj = qs.first()
    if request.method == "POST" :
        serializer = ProfileEditSerializer(instance=profile_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=202)
    serializer = ProfileEditSerializer(instance=profile_obj, context={"request": request})
    return Response(serializer.data, status=200)