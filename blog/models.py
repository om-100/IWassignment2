from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    image = models.ImageField(blank=True, upload_to='profile')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Blog(TimeStamp):
    title = models.CharField(max_length=150, blank=False)
    image = models.ImageField(blank=False, upload_to='blog')
    content = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# class Author(TimeStamp):
#     author = models.OneToOneField(Blog, on_delete=models.CASCADE)
#     name = models.CharField(max_length=150, blank=False)
#
#     def __str__(self):
#         return self.name
