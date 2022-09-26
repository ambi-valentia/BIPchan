from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import Thread

# Create your views here.
def thread_view(request, thread, *args, **kwargs):
    user = None
    if request.user.is_authenticated:
        user = request.user.username

    qs = Thread.objects.filter(name=thread)
    if not qs.exists():
        raise Http404
    thread_obj = qs.first()
    is_subscribed = False
    
    if request.user.is_authenticated:
        user = request.user.profile
        is_subscribed = user in thread_obj.subscribers.all()
    context = {
        "user": user,
        "thread": thread_obj,
        "is_subscribed": is_subscribed
    }
    return render(request,
        "pages/thread.html", 
        context,
        status=200)