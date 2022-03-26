from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'w3-input w3-margin-bottom'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'w3-input w3-margin-bottom'}))