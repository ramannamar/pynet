from django.contrib.auth.models import AbstractUser
from django.db import models


class UserNet(AbstractUser):
    """Custom user model """
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female')
    )

    middle_name = models.CharField(max_length=50, null=True, blank=True)
    first_login = models.DateTimeField(null=True)
    phone_number = models.CharField(max_length=14, null=True)
    avatar = models.ImageField(upload_to='user/avatar/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    github = models.CharField(max_length=500, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male')
