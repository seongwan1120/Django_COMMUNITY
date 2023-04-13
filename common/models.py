from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from discussion.models import Posting, Comment
# Create your models here.

class User(AbstractUser):
    postings_best= models.ManyToManyField(Posting, related_name='users_best')
    postings_worst = models.ManyToManyField(Posting, related_name='users_worst')
    comments_agree = models.ManyToManyField(Comment, related_name='users_agree')
    comments_disagree = models.ManyToManyField(Comment, related_name='users_disagree')
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')