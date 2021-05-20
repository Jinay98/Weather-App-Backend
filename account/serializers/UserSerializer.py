import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers


from account.models import AppUser


class UserSerializer(serializers.ModelSerializer):
    pass

    def create(self, validate_data):
        instance = AppUser.objects.create_user(**validate_data)
        return instance

    def validate(self, data):

        phone_regex = re.compile(r'^[1-9]\d{9}$')
        if not phone_regex.match(data['phone_number']):
            raise serializers.ValidationError(
                {"phone_number": "Phone Number should be of 10 digits"})

        password_regex = re.compile(r'[A-Za-z0-9@#$%^&+=]{8,}')
        if not password_regex.match(data['password']):
            raise serializers.ValidationError({"password": "Enter a strong password!"})

        email = data.get("email", None)
        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError({"email": "Invalid Email Entered"})

        return data

    class Meta:
        model = AppUser
        fields = ['phone_number', 'password', 'email', 'date_joined', 'last_login',
                  'is_admin', 'is_active', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True}
        }
