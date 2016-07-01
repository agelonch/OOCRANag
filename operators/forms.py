from django import forms
from .models import Operator
from django.contrib.auth.forms import AuthenticationForm 
from django import forms

class SettingsForm(forms.ModelForm):
	class Meta:
		model = Operator
		fields = [
			"mcs",
		]