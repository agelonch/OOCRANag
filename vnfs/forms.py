from django import forms
from .models import Vnf


class VnfForm(forms.ModelForm):
    class Meta:
        model = Vnf
        fields = [
            "name",
            "description",
            "image",
            "script",
        ]
