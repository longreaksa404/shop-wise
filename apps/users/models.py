from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from apps.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        SELLER = 'seller', 'Seller'
        BUYER = 'buyer', 'Buyer'

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.BUYER)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # change to log in with email instead of username
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'user'
        ordering = ['-created_at']
        # Set django admin panel
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f"{self.username} ({self.role})"

    # for call like as an attribute instead of method
    @property
    def is_admin(self):
        return self.role == User.Role.ADMIN

    @property
    def is_seller(self):
        return self.role == User.Role.SELLER
    @property
    def is_buyer(self):
        return self.role == User.Role.BUYER
