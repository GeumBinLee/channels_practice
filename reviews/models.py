from django.db import models
from django.core.validators import MaxValueValidator

from users.models import User
from places.models import Place



class Review(models.Model):
    title = models.CharField('제목', max_length=50)
    content = models.TextField('내용', max_length=500)
    review_image_one = models.ImageField('이미지 1', upload_to='review_pics', blank=True)
    review_image_two = models.ImageField('이미지 2', upload_to='review_pics', blank=True)
    review_image_three = models.ImageField('이미지 3', upload_to='review_pics', blank=True)
    created_at = models.DateTimeField('후기 생성 시간', auto_now_add=True)
    updated_at = models.DateTimeField('후기 수정 시간', auto_now=True)
    rating_cnt = models.PositiveIntegerField('별점', validators=[MaxValueValidator(5)])
    
    review_like = models.ManyToManyField(User, verbose_name='후기 좋아요', related_name="like_review", blank=True)

    author = models.ForeignKey(User, verbose_name='작성자', on_delete=models.CASCADE)
    place = models.ForeignKey(Place, verbose_name='장소', on_delete=models.CASCADE)

    class Meta:
        db_table = 'review'

    def __str__(self):
        return f'[작성자]{self.author}, [제목]{self.title}'

class Comment(models.Model):
    content = models.TextField('내용', max_length=100)
    created_at = models.DateTimeField('생성 시간', auto_now_add=True)
    updated_at = models.DateTimeField('수정 시간', auto_now=True)

    comment_like = models.ManyToManyField(User, verbose_name='댓글 좋아요', related_name="like_comment", blank=True)

    author = models.ForeignKey(User, verbose_name='작성자', on_delete=models.CASCADE)
    review = models.ForeignKey(Review, verbose_name='후기', on_delete=models.CASCADE, related_name="review_comments")

    class Meta:
        db_table = 'review_comment'
        ordering = ['-created_at']
        
    def __str__(self):
        return f'[후기 제목]{self.review.title}, [댓글 작성자]{self.author}, [댓글 내용]{self.content}'

class Recomment(models.Model):
    content = models.TextField('내용', max_length=100)
    created_at = models.DateTimeField('생성 시간', auto_now_add=True)
    updated_at = models.DateTimeField('수정 시간', auto_now=True)

    recomment_like = models.ManyToManyField(User, verbose_name='대댓글 좋아요', related_name="like_recomment", blank=True)

    author = models.ForeignKey(User, verbose_name='작성자', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, verbose_name='댓글', on_delete=models.CASCADE, related_name="comment_recomments")

    class Meta:
        db_table = 'review_recomment'
        ordering = ['-created_at']
        
    def __str__(self):
        return f'[후기 제목]{self.comment.review.title}, [대댓글 작성자]{self.author}, [대댓글 내용]{self.content}'
