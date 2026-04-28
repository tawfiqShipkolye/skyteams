from django.contrib import admin
from .models import Message

# Author: Student 3 - Tawfiq
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'sender', 'created_at', 'is_draft', 'is_read']
    list_filter = ['is_draft', 'is_read']
    search_fields = ['subject', 'sender__username']