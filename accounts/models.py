from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email=models.EmailField(unique=True)
    bio=models.TextField(blank=True)
    github_url=models.URLField(blank=True)
    linkedin_url=models.URLField(blank=True)
    batch=models.CharField(max_length=20)
    profile_picture=models.ImageField(upload_to='profiles/',blank=True,null=True)

    def __str__(self):
        return self.username