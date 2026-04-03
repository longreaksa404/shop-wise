from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Require email')
        if not username:
            raise ValueError('Require username')
        email = self.normalize_email(email) # convert to lowercases email format and prevent duplicate
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Is staff must true')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Is superuser must true')

        return self.create_user(email, username, password, **extra_fields)