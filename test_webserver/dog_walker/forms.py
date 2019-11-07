from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class IsTrainerForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['is_trainer']
        labels = {'is_trainer': 'Are you a dog trainer?'}