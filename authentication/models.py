import jwt

from datetime import datetime
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    """ Django requires custom `User` defined their own Manager class.

    By inheriting from BaseUserManager, used by Django to create `User`.
    """
    def _create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The specified username must be set.')

        if not email:
            raise ValueError('This email address must be set.')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password=None, **extra_fields):
        """Creates and returns a `User` with an email address,
        username and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        """Creates and returns a user with rights
        superuser (administrator).
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('The superuser must have is_superuser = True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Defines our custom User class.

    Username, email and password are required.
    """
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(
        validators=[validators.validate_email],
        unique=True,
        blank=False
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # The `USERNAME_FIELD` property tells us which field we will use for login.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    # Tells Django that the UserManager class is definitely above,
    # must manage objects of this type.
    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        """Allows us to get the user's token by calling `user.token`
        instead of user.generate_jwt_token ().
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """This method is required by Django for things like this,
         how to handle email.
         This is usually the user's first and last name.
         Since we do not store the real username, we return his username.
         """
        return self.username

    def get_short_name(self):
        """This method is required by Django for things like this,
         how to handle email.
         This is usually the user's first and last name.
         Since we do not store the real username, we return his username.
         """
        return self.username

    def _generate_jwt_token(self):
        """Creates a JSON web token that stores an ID
         this user and its validity period
         is 60 days in the future.
         """
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
