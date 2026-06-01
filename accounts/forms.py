from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'batch',
            'bio',
            'github_url',
            'linkedin_url',
            'profile_picture',
        ]

class LoginForm(AuthenticationForm):
    pass