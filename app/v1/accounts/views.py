from rest_framework.response import Response
from .models import Accounts
from .serializers import SignupSerializer, LoginSerializer
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from config.constants import ERR_DB, ERR_LOGIN_FAILED, ERR_TOKEN_FAILED, MSG_SIGNUP_SUCCESS, MSG_LOGIN_SUCCESS


class AccountViewset(viewsets.ViewSet):
    """
    회원과 관련된 요청(회원가입, 로그인)을 수행하는 클래스
    """
    queryset = Accounts.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """
        회원가입
        email : '@' 포함 + 기존 아이디 안됨
        pw : 8 글자 이상
        """
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
        except Exception as e:
            print(e)
            return Response({'message': ERR_DB}, status=500)
        return Response({'message': MSG_SIGNUP_SUCCESS})

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        로그인
        email : '@' 포함
        pw : 8 글자 이상
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(email=request.data.get(
            'email'), password=request.data.get('password'))
        if user:
            user.last_login = timezone.now()  # last_login 갱신
            try:
                user.save(update_fields=['last_login'])
            except Exception as e:
                print(e)
                return Response({'message': ERR_DB}, status=500)
            try:
                token = TokenObtainPairSerializer.get_token(user)
                refresh_token = str(token)
                access_token = str(token.access_token)
                return Response({'message': MSG_LOGIN_SUCCESS, 'access_token': access_token, 'refresh_token': refresh_token})
            except Exception as e:
                print(e)
                return Response({'message': ERR_TOKEN_FAILED}, status=500)
        else:
            return Response({'message': ERR_LOGIN_FAILED}, status=400)
