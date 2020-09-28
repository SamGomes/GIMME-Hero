 
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms

from GIMMEWeb.core.models import UserProfile



class CreateUserForm(UserCreationForm):
	# email = models.EmailField(required = True)
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class CreateUserProfileForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ['role', 'fullName', 'age', 'gender', 'description', 'avatar']



class UpdateUserForm(UserChangeForm):
	# email = models.EmailField(required = True)
	class Meta:
		model = User
		fields = ['email']


class UpdateUserProfileForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ['fullName', 'age', 'gender', 'description', 'avatar']




