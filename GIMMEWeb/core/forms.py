 
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms

from GIMMEWeb.core.models import UserProfile, Task, LikertQuestion, Questionnaire, LikertResponse



class DateInput(forms.DateInput):
	input_type = 'date'


class CreateUserForm(UserCreationForm):
	# email = models.EmailField(required = True)
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class CreateUserProfileForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ['role', 'fullName', 'age', 'gender', 'description', 'avatar']

class CreateTaskForm(ModelForm):
	initDate = forms.DateField(widget=DateInput)
	finalDate = forms.DateField(widget=DateInput)
	#minReqAbility = forms.FloatField(required=False, max_value=1.0, min_value=0.0, 
#widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"})) 
	#difficultyWeight = forms.FloatField(required=False, max_value=1.0, min_value=0.0, 
#widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"})) 
	#profileWeight = forms.FloatField(required=False, max_value=1.0, min_value=0.0, 
#widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"})) 
	
	class Meta:
		model = Task
		exclude = ['creator', 'creationTime', 'profile', 'initDate', 'finalDate', 'minReqAbility', 'difficultyWeight', 'profileWeight'] 


class LikertForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for question in LikertQuestion.objects.all():
			self.fields[f"question_{question.id}"] = forms.ChoiceField(
				choices=[(1, '1 (Strongly Disagree)'), (2, '2 (Disagree)'), (3, '3 (Neutral)'), (4, '4 (Agree)'), (5, '5 (Strongly Agree)')],
				widget=forms.RadioSelect,
				label=question.text,
			)


class LikertResponseForm(forms.Form):
    class Meta:
        model = LikertResponse
        fields = ['response']
        widgets = {
            'response': forms.RadioSelect(choices=((1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Neutral'), (4, 'Agree'), (5, 'Strongly Agree')))
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # question_text = kwargs.pop('question.text')
        # self.fields['response'].label = question_text


class UpdateUserForm(UserChangeForm):
	# email = models.EmailField(required = True)
	class Meta:
		model = User
		fields = ['email']


class UpdateUserProfileForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ['fullName', 'age', 'gender', 'description', 'avatar']



class UpdateTaskForm(ModelForm):
	initDate = forms.DateField(widget=DateInput)
	finalDate = forms.DateField(widget=DateInput)
	minReqAbility = forms.FloatField(required=False, max_value=1.0, min_value=0.0, 
widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"})) 
	difficultyWeight = forms.FloatField(required=False, max_value=1.0, min_value=0.0, 
widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"})) 
	profileWeight = forms.FloatField(required=False, max_value=1.0, min_value=0.0, 
widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"})) 
	
	class Meta:
		model = Task
		exclude = ['creator', 'creationTime'] 


