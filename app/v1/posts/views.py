from rest_framework.response import Response
from .models import Posts
from .serializers import PostSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from config.paginations import PostPagination
from config.permissions import IsPostOwnerOrReadOnly


class PostViewset(viewsets.ModelViewSet):
    """
    게시글 CRUD와 관련한 api를 수행하는 클래스
    """
    queryset = Posts.objects.all()
    # 인증되지 않았다면 읽기만 가능 & 본인의 글만 수정 가능
    permission_classes = [IsAuthenticatedOrReadOnly, IsPostOwnerOrReadOnly]
    serializer_class = PostSerializer
    pagination_class = PostPagination  # 10개씩 pagination

    def perform_create(self, serializer):
        """
        글 작성시, author 인증 정보(jwt) 를 통하여 넣어준다
        """
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True  # for partial update
        return super().update(request, *args, **kwargs)
