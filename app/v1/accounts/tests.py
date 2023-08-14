from django.test import TestCase

# Create your tests here.


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