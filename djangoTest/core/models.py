import uuid
from django.db import models

class User(models.Model):
    IMAGE = u'image'

    username = models.CharField(primary_key=True, max_length=255)
    isAuthenticated = models.BooleanField(default=False)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    preferences = models.CharField(max_length=255)
    # email = models.URLField(max_length=500, null=True, blank=True)
    class Meta:
        verbose_name = u'User'
        verbose_name_plural = u'User'
        ordering = ('name',)

   
