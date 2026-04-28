from django import forms
from .models import Message
from django.contrib.auth import get_user_model

# Author: Student 3 - Tawfiq

User = get_user_model()

class MessageForm(forms.ModelForm):
    recipients = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        help_text='Hold Ctrl (Windows) or Cmd (Mac) to select multiple recipients'
    )
    subject = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6})
    )

    class Meta:
        model = Message
        fields = ['recipients', 'subject', 'body']