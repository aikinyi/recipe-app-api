from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):
    """
    Creating Base Manager
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        creating custom user function
        """
        if not email:
            raise ValueError('Email address must be valide')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
        
    def create_superuser(self, email, password):
        """
        Creating superuser method
        """
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Creating model for custom user
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """
    Model for creating
    """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        """String representation for returning name"""
        return self.name


class Ingredient(models.Model):
    """
    Model for creating new ingredient
    """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        """
        Returning default value
        """
        return self.name
