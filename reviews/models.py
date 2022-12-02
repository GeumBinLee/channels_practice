from django.db import models

from users.models import User
from places.models import Place

class Review(models.Model):
    title = models.TextField('제목', max_length=100)
    content = models.TextField('내용', max_length=100)
    created_at = models.DateTimeField('후기 생성 시간', auto_now_add=True)
    updated_at = models.DateTimeField('후기 수정 시간', auto_now = True)
    rating_cnt = models.PositiveIntegerField('별점')
    
    review_like = models.ManyToManyField(User, verbose_name='후기 좋아요', related_name="like_review",blank=True)
    user = models.ForeignKey(User, verbose_name='작성자', on_delete=models.CASCADE, null=True)
    place = models.ForeignKey(Place, verbose_name='장소', on_delete=models.CASCADE)

    class Meta:
        db_table = 'review'

    def __str__(self):
        return f'[제목]{self.title}'
