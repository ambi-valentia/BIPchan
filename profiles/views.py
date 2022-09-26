from django.http import Http404
from django.shortcuts import render, redirect

from .forms import ProfileForm
from .serializers import ProfileEditSerializer
from .models import Profile

def profile_update_view(request, *args, **kwargs):
    if not request.user.is_authenticated: # is_authenticated()
        return redirect("/login?next=/profile/update")
    user = request.user
    my_profile = user.profile
    if request.POST:
        serializer = ProfileEditSerializer(instance=my_profile, data=request.POST)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    else:
        serializer = ProfileEditSerializer(instance=my_profile)
    context = {
        "form": ProfileForm(initial=serializer.data),
        "btn_label": "Save",
        "title": "My Profile"
    }
    return render(request, "profiles/form.html", context)


def profile_detail_view(request, username, *args, **kwargs):
    user = None
    if request.user.is_authenticated:
        user = request.user.username

    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        raise Http404

    profile_obj = qs.first()
    is_following = False
    if request.user.is_authenticated:
        me = request.user
        is_following = me in profile_obj.followers.all()
        
    context = {
        "user" : user,
        "seacrch_user": username,
        "profile": profile_obj,
        "is_following": is_following
    }
    return render(request, "profiles/detail.html", context)
