from django import forms
from .models import Escuela

class FormNewEsc(forms.Form):
        name=forms.CharField(label="Nombre", max_length=100, min_length=5, required=True)
