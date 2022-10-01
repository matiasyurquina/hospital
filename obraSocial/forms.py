from django import forms
from .models import ObraSocial

class FormNewObra(forms.Form):
        name=forms.CharField(label="Nombre", max_length=100, min_length=5, required=True)
