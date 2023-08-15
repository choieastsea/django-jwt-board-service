from rest_framework import permissions

class IsPostOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT','DELETE']:
            # 작성자만 수정, 삭제를 허용
            return obj.author == request.user
        return True # 나머지는 이전 권한 이후에 넘어오는 것이므로 허용