from django import forms
from .models import Deployment

from django.contrib.auth.forms import AuthenticationForm
from django import forms


class DeploymentForm(forms.ModelForm):
    class Meta:
        model = Deployment
        fields = [
            # "area",
            "name",
            "file",
            # "start",
            "stop",
        ]


class AddForm(forms.ModelForm):
    class Meta:
        model = Deployment
        fields = [
            # "area",
            "name",
            "file",
        ]


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))
