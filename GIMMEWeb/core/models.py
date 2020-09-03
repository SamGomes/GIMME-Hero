import uuid
from django.db import models

class User(models.Model):
    userId = models.CharField(primary_key=True, max_length=255)
    isAuthenticated = models.BooleanField(default=False)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    
    fullName = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    preferences = models.CharField(max_length=255)


    currState = models.CharField(max_length=255)
    pastModelIncreasesGrid = models.CharField(max_length=255)
    personality = models.CharField(max_length=255)


    avatar = models.ImageField(upload_to='images/userAvatars/')

class Task(models.Model):
    taskId = models.CharField(primary_key=True, max_length=255)
    
    creator = models.CharField(max_length=255)
    creationTime = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    minReqAbility = models.CharField(max_length=255)
    profile = models.CharField(max_length=255)
    profileImportance = models.CharField(max_length=255)
    difficultyImportance = models.CharField(max_length=255)


    initDate = models.CharField(max_length=255)
    finalDate = models.CharField(max_length=255)


    filePaths = models.CharField(max_length=255)


class ServerState(models.Model):
    currAdaptationState = models.CharField(max_length=255, default="[]")

    currSelectedUsers = models.CharField(max_length=255, default="[]")
    currFreeUsers = models.CharField(max_length=255, default="[]")

    currSelectedTasks = models.CharField(max_length=255, default="[]")
    currFreeTasks = models.CharField(max_length=255, default="[]")

    readyForNewActivity = models.CharField(max_length=255, default="false")

    initDate = models.CharField(max_length=255, default="[]")
    finalDate = models.CharField(max_length=255, default="[]")
