from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    nickname=models.CharField(max_length=20, blank=False, null= False)
    kakao_id = models.CharField(max_length=255, unique=True, null= True)
    # phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions_set", blank=True)

