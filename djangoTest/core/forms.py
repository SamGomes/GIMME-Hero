from django import forms
from djangoTest.core.models import User

class RegistryForm(forms.Form):
	id = forms.IntegerField(default=-1,primary_key=True)
    role = forms.CharField(max_length=255)
    name = forms.CharField(max_length=255)
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)
    age = forms.IntegerField(default=-1)
    gender = forms.CharField(max_length=255)
    preferences = forms.CharField(max_length=255)
    email = forms.URLField(max_length=500, null=True, blank=True)