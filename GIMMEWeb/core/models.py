import os
from uuid import uuid4

from enum import Enum
from enumfields import EnumField

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from multiselectfield import MultiSelectField

from django.core.validators import MaxValueValidator, MinValueValidator

ROLE = (('Developer', 'Developer'),
        ('Professor', 'Professor'),
        ('Student', 'Student'))

GENDER = (('Male', 'Male'),
          ('Female', 'Female'),
          ('Other', 'Other'))


class QuestionnaireType(Enum):
    MBTI = 'MBTI'


QUESTIONNAIRE_TYPES = ((QuestionnaireType.MBTI, 'MBTI'))


class ModelAuxMethods:
    def path_and_rename(path):
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


class Questionnaire(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=3072)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    type = EnumField(QuestionnaireType)
    dashboard_message = models.TextField(max_length=3072)


class Submission(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class LikertQuestion(models.Model):
    left_extremity = models.TextField(max_length=127)
    right_extremity = models.TextField(max_length=127)


class LikertQuestionnaire(Questionnaire):
    questions = models.ManyToManyField(LikertQuestion, related_name='questionnaires')


class LikertResponse(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(LikertQuestion, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(
        choices=((1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Neutral'), (4, 'Agree'), (5, 'Strongly Agree')))


class Tag(models.Model):
    name = models.CharField(max_length=32)
    target = models.CharField(max_length=32)
    is_selected = models.BooleanField(default=False)
    is_removable = models.BooleanField(default=True)
    is_assignable = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    # included from 
    # https://stackoverflow.com/questions/15140942/django-imagefield-change-file-name-on-upload

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                db_constraint=False)

    role = MultiSelectField(choices=ROLE, max_choices=1, max_length=9)

    fullname = models.CharField(max_length=1020)
    age = models.IntegerField()
    gender = MultiSelectField(choices=GENDER, max_choices=1, max_length=6)
    description = models.TextField(blank=True, max_length=3072)

    curr_state = models.TextField(max_length=3072)
    past_data_frame = models.TextField(max_length=3072)
    preferences = models.CharField(max_length=1020)
    personality = models.CharField(max_length=1020)

    characteristics = models.CharField(max_length=1020)

    tags = models.ManyToManyField(Tag)

    # subjectIds = models.CharField(max_length=1020)
    grade = models.CharField(max_length=1020)

    avatar = models.ImageField(upload_to=ModelAuxMethods.path_and_rename('images/userAvatars/'),
                               default='images/userAvatars/avatarPH.png')

    def __str__(self):
        return self.user.username


class Task(models.Model):
    task_id = models.CharField(max_length=100, primary_key=True)

    creator = models.CharField(max_length=1020)
    creation_time = models.CharField(max_length=1020)
    description = models.TextField(blank=True, max_length=3072)
    min_req_ability = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    profile = models.CharField(max_length=1020)

    profile_w = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    difficulty_w = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

    init_date = models.DateField()
    final_date = models.DateField()

    files = models.FileField(upload_to=ModelAuxMethods.path_and_rename('taskFiles/'), default='taskFiles/placeholder')

    tags = models.ManyToManyField(Tag)
    
    def __str__(self):
        return self.task_id


class ServerState(models.Model):
    curr_adaptation_state = models.TextField(max_length=3072, default="[]")

    curr_selected_users = models.TextField(max_length=3072, default="[]")
    curr_free_users = models.TextField(max_length=3072, default="[]")

    curr_selected_tasks = models.TextField(max_length=3072, default="[]")
    curr_free_tasks = models.TextField(max_length=3072, default="[]")

    ready_for_new_activity = models.CharField(max_length=1020, default="false")

    init_date = models.CharField(max_length=1020, default="[]")
    final_date = models.CharField(max_length=1020, default="[]")

    sim_is_link_shared = models.BooleanField(default=False)
    sim_is_task_created = models.BooleanField(default=False)
    sim_week_one_users_evaluated = models.BooleanField(default=False)
    sim_simulate_reaction = models.BooleanField(default=False)
    sim_week_four_done_once = models.BooleanField(default=False)

    simulation_week = models.IntegerField(default=0)
    sim_student_to_evaluate = models.CharField(max_length=1020)
    sim_unavailable_student = models.CharField(max_length=1020)
    sim_student_x = models.CharField(max_length=1020)
    sim_student_y = models.CharField(max_length=1020)
    sim_student_w = models.CharField(max_length=1020)
    sim_student_z = models.CharField(max_length=1020)
    def __str__(self):
        return self.id
