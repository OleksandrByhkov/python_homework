from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    preferred_language = models.CharField(max_length=5, choices=(("uk", "Українська"), ("en", "English")), default="uk")
