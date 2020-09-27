import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):

    user = models.OneToOneField(User, 
        on_delete=models.CASCADE,
        primary_key=True)

    # email = models.CharField(max_length=255)
    # password = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    
    fullName = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


    currState = models.CharField(max_length=255)
    pastModelIncreasesGrid = models.CharField(max_length=255)
    personality = models.CharField(max_length=255)


    avatar = models.ImageField(upload_to='images/userAvatars/')


    def create_profile(sender, **kwargs):
        if kwargs['created']:
            args = kwargs['instance']
            user_profile = UserProfile.objects.create(user = kwargs['instance'])
            #     user = kwargs['instance'], 
            #     role = args.role, 
            #     fullName = args.fullName, 
            #     age = args.age, 
            #     gender = args.gender, 
            #     description = args.description, 
            #     currState = args.currState, 
            #     pastModelIncreasesGrid = args.pastModelIncreasesGrid, 
            #     personality = args.personality, 
            #     avatar = args.avatar
            # ) 

    post_save.connect(create_profile, sender=User)


    # def __str__(self):
    #     return self.userId


class Task(models.Model):
    taskId = models.CharField(primary_key=True, max_length=255)
    
    creator = models.CharField(max_length=255)
    creationTime = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    minReqAbility = models.CharField(max_length=255)
    profile = models.CharField(max_length=255)
    
    profileWeight = models.CharField(max_length=255)
    difficultyWeight = models.CharField(max_length=255)


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
