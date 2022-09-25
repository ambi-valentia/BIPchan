import random
from threads.models import Thread
from django.conf import settings
from django.db import models
from django.db.models import Q
from threads.models import Thread

User = settings.AUTH_USER_MODEL

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey("Message", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class MessageQuerySet(models.QuerySet):
    def feed(self, user):
        profile = user.profile
        profiles_exist = user.following.exists()
        followed_users_id = []
        if profiles_exist:
            followed_users_id = user.following.values_list("user__id", flat=True)
        subscriptions_exist = profile.subscriptions.exists()
        threads_id = []
        if subscriptions_exist:
            threads_id = profile.subscriptions.values_list("id", flat=True)
        return self.filter(
            Q(user__id__in=followed_users_id) |
            Q(thread__id__in=threads_id)|
            Q(user=user)
        ).distinct().order_by("-timestamp")

class MessageManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return MessageQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes', blank=True, through=Like)
    content = models.TextField(blank=True, null=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = MessageManager()
    class Meta:
        ordering = ['-id']

