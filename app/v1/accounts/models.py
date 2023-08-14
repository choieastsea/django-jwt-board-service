# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class AccountsManager(BaseUserManager):
    """
    Manager class for AbstractBaseUser class 'Accounts'
    super user와 manager는 만들지 않았다
    """

    def create_user(self, email, password=None):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user


class Accounts(AbstractBaseUser):
    """
    User Class
    - fields : [id, email, password, last_login, created_at, updated_at]
    """

    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountsManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'accounts'
