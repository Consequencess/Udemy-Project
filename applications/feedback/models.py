from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from applications.course.models import Course

User = get_user_model()


class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], blank=True,
                                              null=True)


class Comment(models.Model):
    comment = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')


class LikeDislikeComment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_comments')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='like_comments')
    like = models.BooleanField(default=False)


class Wishlist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='wishlist')


