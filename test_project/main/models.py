from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    text = models.CharField(max_length=50)
    author = models.ForeignKey(User)
