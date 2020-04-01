import uuid
from django.db import models

class User(models.Model):
    IMAGE = u'image'

    username = models.CharField(primary_key=True, max_length=255)
    isAuthenticated = models.BooleanField(default=False)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    
    fullName = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    preferences = models.CharField(max_length=255)


    currState = models.CharField(max_length=255)
    pastModelIncreasesGrid = models.CharField(max_length=255)
    personality = models.CharField(max_length=255)

    # email = models.URLField(max_length=500, null=True, blank=True)
    # class Meta:
    #     verbose_name = u'User'
    #     verbose_name_plural = u'User'

class Task(models.Model):
    IMAGE = u'image'

    id = models.CharField(primary_key=True, max_length=255)
    
    description = models.CharField(max_length=255)
    minReqAbility = models.CharField(max_length=255)
    profile = models.CharField(max_length=255)
    profileImportance = models.CharField(max_length=255)
    difficultyImportance = models.CharField(max_length=255)



class ServerState(models.Model):
    currAdaptationState = models.CharField(max_length=255, default="[]")
    currWaitingPlayers = models.CharField(max_length=255, default="[]")
    currOccupiedPlayers = models.CharField(max_length=255, default="[]")
    readyForNewActivity = models.CharField(max_length=255, default="false")
