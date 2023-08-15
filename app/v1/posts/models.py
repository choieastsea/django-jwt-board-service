from django.db import models
from django.conf import settings

# Create your models here.


class Posts(models.Model):
    """
    Table posts {
        post_id integer [primary key]
        title varchar
        author_id integer
        body text
        created_at timestamp
        updated_at timestamp
    }
    """
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE) # user 삭제시 post 삭제
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post_id

    class Meta:
        db_table = 'posts'