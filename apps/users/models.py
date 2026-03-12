from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Require email')
        if not username:
            raise ValueError('Require username')
        email = self.normalize_email(email) # convert to lowercases email format and prevent duplicate
        user = self.model(email=email,username=username, **extra_fields)
        user.set_password(password) #hash password
        user.save(using=self._db)
        return user
    def create_superuser(self, ema8il, username, password=None, **extra_fields):
