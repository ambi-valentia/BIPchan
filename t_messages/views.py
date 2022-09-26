import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    user = None
    if request.user.is_authenticated:
        user = request.user.username
    return render(request,
        "pages/home.html", 
        context = {
            "user" : user
        },
        status=200)

# Create your views here.
def feed_view(request, *args, **kwargs):
    user = None
    if request.user.is_authenticated:
        user = request.user.username
    return render(request,
        "pages/feed.html", 
        context = {
            "user" : user
        },
        status=200)

def search_view(request,*args, **kwargs):
    user = None
    if request.user.is_authenticated:
        user = request.user.username
    search_query = request.GET.get('search', '')
    return render(request,
        "pages/search.html", 
        context = {
            "user" : user,
            "search_query" : search_query
        },
        status=200)