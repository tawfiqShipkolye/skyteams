from django.contrib.auth.models import AbstractUser
from django.db import models

# Author: Student 3 - Tawfiq
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username