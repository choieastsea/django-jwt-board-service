from rest_framework.serializers import ModelSerializer, CharField
from .models import Posts


class PostSerializer(ModelSerializer):
    """
    게시글의 CRUD와 관련된 validation 수행
    post (역)직렬화 수행
    """
    author = CharField(read_only=True) # accounts.toString(Accounts(id=?)) 수행된 결과가 직렬화 과정에서 들어가게 될것 -> email

    class Meta:
        model = Posts
        fields = "__all__"
