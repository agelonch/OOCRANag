from django import forms
from .models import Client

from django.contrib.auth.forms import AuthenticationForm 
from django import forms

class UserForm(forms.Form):
	name = forms.CharField(label='name', max_length=100)
	file = forms.FileField(label='file')
