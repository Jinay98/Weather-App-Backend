import re

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.validators import validate_email
from django.db import models


class AppAccountManager(BaseUserManager):
    def create_user(self, phone_number, email, password=None):

        if not phone_number:
            raise ValueError('Users must have a phone number')
        is_valid_phone_number = self.validatePhoneNumber(phone_number)
        if not is_valid_phone_number:
            raise ValueError('Phone Number is not valid')

        if not email:
            raise ValueError('Users must have an Email ID')
        is_valid_email = self.validateEmail(email)
        if not is_valid_email:
            raise ValueError('Email is not valid')

        user = self.model(phone_number=phone_number, email=email)

        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, password):
        user = self.create_user(phone_number=phone_number, email=email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def validatePhoneNumber(self, phone_number):
        phone_regex = re.compile(r'^[1-9]\d{9}$')
        return phone_regex.match(phone_number)

    def validateEmail(self, email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False


class AppUser(AbstractBaseUser):
    username = None
    phone_regex = RegexValidator(regex=r'^[1-9]\d{9}$', message="Phone number must contain 10 digits")
    phone_number = models.CharField(verbose_name="phone number", validators=[phone_regex], max_length=15, unique=True)
    email = models.EmailField(verbose_name="email", max_length=60)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    objects = AppAccountManager()

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
