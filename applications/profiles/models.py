from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()


class Profile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')
    competence = models.CharField(max_length=128)
    language = models.CharField(max_length=128)
    site_url = models.CharField(max_length=128)
    twitter_url = models.CharField(max_length=128)
    facebook_url = models.CharField(max_length=128)
    linkedin_url = models.CharField(max_length=128)
    youtube_url = models.CharField(max_length=128)
    image = models.CharField(max_length=128)
    is_hidden = models.BooleanField(default=False, blank=True)
    is_hidden_courses = models.BooleanField(default=False, blank=True)
    promotions = models.BooleanField(default=False, blank=True)
    mentor_abs = models.BooleanField(default=False, blank=True)
    email_abs = models.BooleanField(default=False, blank=True)



