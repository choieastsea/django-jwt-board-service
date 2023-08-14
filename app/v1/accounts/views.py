from rest_framework.response import Response
from .models import Accounts
from .serializers import SignupSerializer,LoginSerializer
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django.contrib.auth import authenticate


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
        user = serializer.save()
        return Response({'message': '회원가입성공'})

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        로그인
        email : '@' 포함
        pw : 8 글자 이상
        """
        serializer = LoginSerializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(email=request.data.get(
            'email'), password=request.data.get('password'))
        if user:
            # token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': '로그인 성공!'})
        else:
            return Response({'error': '로그인 실패!'}, status=400)
        