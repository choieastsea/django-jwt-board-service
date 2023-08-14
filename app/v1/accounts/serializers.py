from rest_framework.serializers import ModelSerializer, CharField
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .models import Accounts
from .validators import *

User = get_user_model()


class SignupSerializer(ModelSerializer):
    """
    1. signup과 관련된 validation 수행
    2. create override 
    """
    class Meta:
        model = Accounts
        fields = ("email", "password")

    email = CharField(
        validators=[email_regex_validator, email_unique_validator])
    password = CharField(validators=[password_regex_validator])

    def create(self, validated_data):
        password = validated_data.pop('password')
        # NOT init password in User model (set_password 통해서)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(ModelSerializer):
    """
    login과 관련된 validation 수행
    """
    class Meta:
        model = Accounts
        fields = ("email", "password")
    email = CharField(validators=[email_regex_validator])
    password = CharField(validators=[password_regex_validator])
