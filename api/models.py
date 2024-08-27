# # models.py
# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# import uuid
# from django.db import models
# from .manager import UserManager

# class User(AbstractUser):
#     username=None
#     email=models.EmailField(unique=True)
#     is_varified=models.BooleanField(default=True)
#     otp=models.CharField(max_length=6,null=True,blank=True)
#     USERNAME_FIELD='email'
#     REQUIRED_FIELDS=[]
#     object=UserManager()
#     def __str__(self):
#         return self.email



# models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, **extra_fields):
        """
        Create and return a regular user with the given email.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        # user.set_password(password)  # Remove or comment this line
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.email}-{self.otp}'
