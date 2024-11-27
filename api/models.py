from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Use related_name to resolve conflicts
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # Avoid conflict with auth.User
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # Avoid conflict with auth.User
        blank=True,
    )

    USERNAME_FIELD = 'username'


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
