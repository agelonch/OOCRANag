from django import forms
from .models import Client
from vnfs.models import Vnf
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class UserForm(forms.Form):
    name = forms.CharField(label='Name:', max_length=100)
    file = forms.FileField(label='File:')

    fieldsets = (
        (None, {
            'fields': ('url', 'title', 'content', 'sites')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('registration_required', 'template_name'),
        }),
    )

class VnfForm(forms.ModelForm):
    class Meta:
        model = Vnf
        fields = [
            "name",
            "description",
            "image",
            "script",
        ]
