from django.db import models



class Chat(models.Model):
    content = models.CharField(max_length=30)
    sender = models.CharField(max_length=30, null=True)