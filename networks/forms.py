from django import forms
from .models import Controller

class ControllerForm(forms.ModelForm):
	class Meta:
		model = Controller
		fields = [
			"name",
			"cluster",
			"network",
		]