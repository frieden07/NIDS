"""
Module Name: User Auth.

This module defines the database model for User Profiles in the system.

Contents:
- Profile: A model that extends the Django User model to include additional
  personal information fields such as name, designation, date of birth, gender,
  address, and role. It establishes a one-to-one relationship with the User model.
"""

from django.db import models
from django.contrib.auth.models import User

gender = (
    ("male", "male"),
    ("female", "female"),
)

roles = (
    ("Network Admin", "Network Admin"),
    ("Security Analyst", "Security Analyst"),
    ("Guest", "Guest"),
)


class Profile(models.Model):
    """
    Represents the extended user profile in the system, including personal information
    such as name, designation, date of birth, gender, address, and role. It is linked
    one-to-one with the Django User model.
    """

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=gender, null=True)
    address = models.CharField(max_length=150, null=True)
    role = models.CharField(max_length=255, choices=roles, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True)
    is_active = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
