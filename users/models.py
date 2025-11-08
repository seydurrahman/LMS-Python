from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
USER_ROLES = (
    ('admin', 'Admin'),
    ('teacher', 'Teacher'),
    ('student', 'Student'),
)

class User(AbstractUser):
    role = models.CharField(max_length=10, choices=USER_ROLES)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    

