from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator
from .models import Accounts

email_regex_validator = RegexValidator(
    regex=r'@',
    message='email은 @를 포함해야합니다.')

email_unique_validator = UniqueValidator(
    queryset=Accounts.objects.all(),
    message='해당 이메일로 이미 가입된 내역이 있습니다')

password_regex_validator = RegexValidator(
    regex=r'^.{8,}$',
    message='비밀번호는 8자 이상이여야합니다')
