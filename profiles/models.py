from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from threads.models import Thread

User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    telegram_id = models.IntegerField(blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    subscriptions = models.ManyToManyField(Thread, related_name='subscribers', blank=True)

def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(user_did_save, sender=User)

# after the user logs in -> verify profile