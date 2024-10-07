from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Manager for custom user model."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with the given email and password."""
        if not email:
            raise ValueError(_('The Email field must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    """Custom User Model using email instead of username."""

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Determines if user can log in to the admin site
    token = models.CharField(max_length=1000)
    objects = CustomUserManager()
    address = models.CharField(max_length=500, blank=True, null=True)

    USERNAME_FIELD = 'email'  # Use email to log in
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Fields that are required on the admin page for superusers

    class Meta:
        db_table = 'user'  # Specify the database table name
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email
