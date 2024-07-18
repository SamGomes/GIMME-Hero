from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms

from GIMMEWeb.core.models import UserProfile, Task, LikertQuestion, Questionnaire, LikertResponse, Tag

class LikertChoiceField(forms.ChoiceField):
    def __init__(self, choices, widget, left_extremity, right_extremity):
        super().__init__(choices=choices, widget=widget, label="")
        self.left_extremity = left_extremity
        self.right_extremity = right_extremity


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
        fields = ['role', 'fullname', 'age', 'gender', 'description', 'avatar']


class CreateTaskForm(ModelForm):
    init_date = forms.DateField(widget=DateInput)
    final_date = forms.DateField(widget=DateInput)

    # minReqAbility = forms.FloatField(required=False, max_value=1.0, min_value=0.0, 
    # widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"})) 
    # difficultyWeight = forms.FloatField(required=False, max_value=1.0, min_value=0.0, 
    # widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"})) 
    # profileWeight = forms.FloatField(required=False, max_value=1.0, min_value=0.0, 
    # widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"})) 

    class Meta:
        model = Task
        exclude = ['creator', 'creation_time', 'profile', 'init_date', 'final_date', 'min_req_ability', 'difficulty_w',
                   'profile_w']


class LikertForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for question in LikertQuestion.objects.all():
            self.fields[f"question_{question.id}"] = LikertChoiceField(
                [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
                forms.RadioSelect,
                question.left_extremity,
                question.right_extremity
            )


class CreateTagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


class UpdateUserForm(UserChangeForm):
    # email = models.EmailField(required = True)
    class Meta:
        model = User
        fields = ['email']


class UpdateUserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['fullname', 'age', 'gender', 'description', 'avatar']


class UpdateUserPersonalityForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['personality']


class UpdateTaskForm(ModelForm):
    init_date = forms.DateField(widget=DateInput)
    final_date = forms.DateField(widget=DateInput)
    min_req_ability = forms.FloatField(required=False, max_value=1.0, min_value=0.0,
                                       widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"}))
    difficulty_w = forms.FloatField(required=False, max_value=1.0, min_value=0.0,
                                    widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"}))
    profile_w = forms.FloatField(required=False, max_value=1.0, min_value=0.0,
                                 widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"}))

    class Meta:
        model = Task
        exclude = ['creator', 'creation_time']
