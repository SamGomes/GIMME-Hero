import os
import uuid
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from multiselectfield import MultiSelectField

from django.core.validators import MaxValueValidator, MinValueValidator

from django import forms


ROLE = (('designer', 'designer'),
       ('professor', 'professor'),
       ('student', 'student'))


GENDER = (('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'))


class ModelAuxMethods():

    def pathAndRename(path):
        def wrapper(instance, filename):
            ext = filename.split('.')[-1]
            # get filename
            if instance.pk:
                filename = '{}.{}'.format(instance.pk, ext)
            else:
                # set filename as random string
                filename = '{}.{}'.format(uuid4().hex, ext)
            # return the whole path to the file
            return os.path.join(path, filename)
        return wrapper


class UserProfile(models.Model):

    # included from 
    # https://stackoverflow.com/questions/15140942/django-imagefield-change-file-name-on-upload
  
    user = models.OneToOneField(User, 
        on_delete=models.CASCADE,
        primary_key=True)

    role = MultiSelectField(choices=ROLE, max_choices=1)
    
    fullName = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = MultiSelectField(choices=GENDER, max_choices=1)
    description = models.TextField(max_length=255)


    currState = models.CharField(max_length=255)
    pastModelIncreasesGrid = models.CharField(max_length=255)
    personality = models.CharField(max_length=255)


    avatar = models.ImageField(upload_to=ModelAuxMethods.pathAndRename('images/userAvatars/'))


    def __str__(self):
        return self.user.username




class Task(models.Model):
    taskId = models.CharField(max_length=255,primary_key=True)

    creator = models.CharField(max_length=255)
    creationTime = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    minReqAbility = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    profile = models.CharField(max_length=255)
    
    profileWeight = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    difficultyWeight = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])


    initDate = models.DateField()
    finalDate = models.DateField()


    files = models.FileField(upload_to=ModelAuxMethods.pathAndRename('taskFiles/'))


    def __str__(self):
        return self.taskId

class ServerState(models.Model):
    currAdaptationState = models.CharField(max_length=255, default="[]")

    currSelectedUsers = models.CharField(max_length=255, default="[]")
    currFreeUsers = models.CharField(max_length=255, default="[]")

    currSelectedTasks = models.CharField(max_length=255, default="[]")
    currFreeTasks = models.CharField(max_length=255, default="[]")

    readyForNewActivity = models.CharField(max_length=255, default="false")

    initDate = models.CharField(max_length=255, default="[]")
    finalDate = models.CharField(max_length=255, default="[]")
