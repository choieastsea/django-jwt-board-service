from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator
from .models import Accounts
from config.constants import ERR_EMAIL_INVALID, ERR_EMAIL_DUPLICATED, ERR_PW_INVALID

email_regex_validator = RegexValidator(
    regex=r'@',
    message=ERR_EMAIL_INVALID)

email_unique_validator = UniqueValidator(
    queryset=Accounts.objects.all(),
    message=ERR_EMAIL_DUPLICATED)

password_regex_validator = RegexValidator(
    regex=r'^.{8,}$',
    message=ERR_PW_INVALID)
