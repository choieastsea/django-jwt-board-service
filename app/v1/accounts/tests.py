from django.test import TestCase
from .models import Accounts
from .serializers import SignupSerializer, LoginSerializer
import json


# 1. 회원가입
# 정상 케이스 -> 회원 가입 완료(비밀번호 암호화)
# validation test(아이디, 비밀번호) 만족 못하는 경우
# 아이디 겹치는 경우

# 2. 로그인
# 정상 케이스 ->token 발급
# validation test 만족 못하는 경우

# 3. jwt
# 토큰 인증
# 기간 만료시 token refresh

class AccountsTest(TestCase):

    def setUp(self):
        """
        각 테스트 메소드가 실행되기 이전에 실행되는 함수
        """
        self.email = 'email@test.com'
        self.password = 'password'
        self.user1 = Accounts.objects.create_user(
            email=self.email, password=self.password)

    def tearDown(self) -> None:
        """
        각 테스트 메소드가 실행된 이후에 실행되는 함수
        """
        return super().tearDown()

    def test_signup_basic(self):
        """
        정상 케이스 회원가입 (통합)
        """
        new_email = 'test@test.com'
        new_password = 'newpassword'
        response = self.client.post(
            f'/api/v1/account/signup/', {'email': new_email, 'password': new_password})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Accounts.objects.filter(email=new_email).count(), 1)

    def test_signup_validation(self):
        """
        validation test (serializer test)
        1. 둘 중 하나 없는 경우
        2. id @ 빼먹은 경우
        3. pw 8글자 미만인 경우
        """
        email1 = ''
        password1 = ''
        data = Accounts(email=email1, password=password1)
        serializer = SignupSerializer(data=data)
        self.assertEqual(serializer.is_valid(), False)

        email2 = 'test.com'
        password2 = 'newpassword'
        data = Accounts(email=email2, password=password2)
        serializer = SignupSerializer(data=data)
        self.assertEqual(serializer.is_valid(), False)

        email3 = '@'
        password3 = '1234567'
        data = Accounts(email=email3, password=password3)
        serializer = SignupSerializer(data=data)
        self.assertEqual(serializer.is_valid(), False)

    def test_signup_duplicate(self):
        """
        duplication test
        중복 회원가입 불가능한지 확인
        """
        email = 'email@test.com'  # setUp에서 이미 저장되어 있음
        password = '12345678'
        data = Accounts(email=email, password=password)
        serializer = SignupSerializer(data=data)
        self.assertEqual(serializer.is_valid(), False)

    def test_login_basic(self):
        """
        정상 케이스 로그인 (통합)
        jwt 반환하는지도 확인
        """
        response = self.client.post(
            f'/api/v1/account/login/', {'email': self.email, 'password': self.password})
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertEqual(response['data']['message'], '로그인 성공')
        self.assertEqual(len(response['data']['access_token']) > 0, True)

    def test_login_validation(self):
        """
        1. 둘 중 하나 없는 경우
        2. id @ 빼먹은 경우
        3. pw 8자 미만
        """
        email1 = ''
        password1 = ''
        data = Accounts(email=email1, password=password1)
        serializer = LoginSerializer(data=data)
        self.assertEqual(serializer.is_valid(), False)

        email2 = 'test.com'
        password2 = 'newpassword'
        data = Accounts(email=email2, password=password2)
        serializer = LoginSerializer(data=data)
        self.assertEqual(serializer.is_valid(), False)

        email3 = '@'
        password3 = '1234567'
        data = Accounts(email=email3, password=password3)
        serializer = LoginSerializer(data=data)
        self.assertEqual(serializer.is_valid(), False)
