from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# Author: Student 3 - Tawfiq

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']