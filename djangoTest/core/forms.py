from django import forms
from djangoTest.core.models import User

class RegistryForm(forms.ModelForm):
	class Meta:
		model = User
		exclude = ['id']