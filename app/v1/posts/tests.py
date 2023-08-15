from django.test import TestCase
from .models import Posts
from ..accounts.models import Accounts
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
import json

# 1. 개시물 작성
# 2. 개시물 리스트 with pagination
# 3. 개시물 글 확인 by id
# 4. 개시물 수정 by id + 작성자만 수정 가능
# 5. 개시물 삭제 by id + 작성자만 삭제 가능


class PostsTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.data = {'title': 'test title', 'body': 'test content'}
        self.email = 'email@test.com'
        self.password = 'password'
        self.user = Accounts.objects.create_user(
            email=self.email, password=self.password)
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.email2 = 'email2@test.com'
        self.password2 = 'password'
        self.user2 = Accounts.objects.create_user(
            email=self.email2, password=self.password2)
        self.token2 = str(RefreshToken.for_user(self.user2).access_token)

    def tearDown(self) -> None:
        return super().tearDown()

    def test_create(self):
        """
        개시글 생성 (user로 인증된 상태)
        1. 글 작성 확인
        2. 인증 정보로 author 초기화 확인
        """
        response = self.client.post('/api/v1/post/', self.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Posts.objects.filter(
            title=self.data['title']).count(), 1)
        response = json.loads(response.content)
        self.assertEqual(response['data']['author'], self.email)

    def test_list(self):
        """
        개시글 리스트
        1. 다 보여지는지
        2. pagination 체크 (10개씩)
        """
        post_cnt = 21
        for _ in range(post_cnt):
            self.client.post('/api/v1/post/', self.data)
        response = self.client.get('/api/v1/post/')
        response = json.loads(response.content)
        self.assertEqual(response['data']['count'], post_cnt)
        self.assertEqual(len(response['data']['results']), 10)

    def test_update(self):
        """
        개시글 수정
        1. 본인이 아닌 다른 사람의 글 수정 불가
        2. updated_at 수정되는지
        """
        post = Posts(post_id=1, title='title', body='body', author=self.user)
        post.save()
        # 본인이 바꾸는 것은 가능
        response = self.client.put('/api/v1/post/1/', {"title": "제목 변경1"})
        self.assertEqual(response.status_code, 200)

        # 제목 바뀌었는지
        self.assertEqual(Posts.objects.get(post_id=post.post_id).title, "제목 변경1")
        # updated_at 바뀌었는지
        self.assertNotEqual(Posts.objects.get(post_id=post.post_id).updated_at, Posts.objects.get(post_id=post.post_id).created_at)

        # 남이 바꾸는 것은 불가능
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')
        response = self.client.put('/api/v1/post/1/', {"title": "제목 변경2"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Posts.objects.get(post_id=post.post_id).title, "제목 변경1")

    def test_delete(self):
        """
        개시글 삭제
        1. 본인이 아닌 다른 사람의 글 수정 불가
        """
        post = Posts(post_id=1, title='title', body='body', author=self.user)
        post.save()
        # 본인이 삭제하는 것은 가능
        response = self.client.delete('/api/v1/post/1/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Posts.objects.filter(post_id=post.post_id).count(), 0)

        post.save()
        # 남이 삭제하는 것은 불가능
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')
        response = self.client.delete('/api/v1/post/1/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Posts.objects.filter(post_id=post.post_id).count(), 1)