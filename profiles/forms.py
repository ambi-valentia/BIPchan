from django import forms
from django.contrib.auth import get_user_model

from .models import Profile 

User = get_user_model()

class ProfileForm(forms.Form):
    first_name = forms.CharField(required=False, label="Name")
    last_name = forms.CharField(required=False, label="Surname")
    bio = forms.CharField(required=False, label="Bio", widget=forms.Textarea)
    telegram_id = forms.IntegerField(required=False, label="Telegram ID", min_value=0)
    email = forms.EmailField(required=False, label="E-mail")    