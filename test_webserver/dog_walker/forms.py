from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    isTrainer = forms.BooleanField(label="Are You a Dog Trainer?")


    class Meta:
        model = User
        # fields = ['username', 'email', 'password1', 'password2', 'isTrainer']
        fields = ['username', 'email', 'password1', 'password2']
