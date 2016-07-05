from django import forms
from .models import Bts, Area


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = [
            "name",
            "description",
            "latitude",
            "longitude",
            "file",
            "forecast",
        ]
