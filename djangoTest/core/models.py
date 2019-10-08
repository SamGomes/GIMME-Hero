from django.db import models

class User(models.Model):
    IMAGE = u'image'

    id = models.IntegerField(default=-1,primary_key=True)
    role = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    age = models.IntegerField(default=-1)
    gender = models.CharField(max_length=255)
    preferences = models.CharField(max_length=255)
    email = models.URLField(max_length=500, null=True, blank=True)


    class Meta:
        verbose_name = u'User'
        verbose_name_plural = u'User'
        ordering = ('name',)
