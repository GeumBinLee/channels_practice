from django.db import models



class Notification(models.Model):
    content = models.CharField(max_length=30)