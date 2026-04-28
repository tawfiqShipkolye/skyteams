from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Author: Student 3 - Tawfiq
admin.site.register(CustomUser, UserAdmin)