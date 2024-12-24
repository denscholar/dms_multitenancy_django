from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
import uuid
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta

from tenants.models import Client


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("the Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(user=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, password, and any extra fields.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if extra_fields.get("is_verified") is not True:
            raise ValueError("Superuser must have is_verified=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15, blank=True, null=True)
    slug = models.CharField(max_length=250, unique=True)
    car_number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

     # Establish relationship with Client (tenant)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="users", null=True, blank=True)


    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.phone) + str(uuid.uuid4())

        # Generate a default password if not already set
        # if not self.default_password:
        #     self.default_password = self.generate_default_password()

        # if self.created_at and (timezone.now() - self.created_at) >= timedelta(days=90):
        #     # send an email to the user
        #     self.send_ninety_day_email()
        #     pass
        super().save(*args, **kwargs)
