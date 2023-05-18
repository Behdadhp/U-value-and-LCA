from django import forms
from . import models


class CreateBuilding(forms.ModelForm):
    """Form for creating building"""

    class Meta:
        model = models.Building
        fields = ("name", "project")


class CreateMaterial(forms.ModelForm):
    """Form for creating material"""

    class Meta:
        model = models.Material
        fields = (
            "name",
            "rho",
            "lamb",
            "type",
            "GWP",
            "ODP",
            "POCP",
            "AP",
            "EP",
            "url_to_oekobaudat",
        )
