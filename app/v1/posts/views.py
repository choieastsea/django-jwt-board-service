from rest_framework.response import Response
from .models import Posts
from .serializers import PostSerializer
from rest_framework import viewsets, permissions

class PostViewset(viewsets.ModelViewSet):
    """
    게시글 CRUD와 관련한 api를 수행하는 클래스
    """
    queryset = Posts.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """
        글 작성시, author 인증 정보(jwt) 를 통하여 넣어준다
        """
        serializer.save(author=self.request.user)