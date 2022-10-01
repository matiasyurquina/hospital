from django import forms
from .models import *

class FormNewPerson(forms.Form):
    name=forms.CharField(label="Nombre", max_length=100, min_length=2, required=True)
    lname=forms.CharField(label="Apellido", max_length=100, min_length=2, required=True)
    dni=forms.IntegerField(label="DNI", required=True)
    cel=forms.IntegerField(label="Celular", required=False)
    dir=forms.CharField(label="Dirección", max_length=100, min_length=3, required=True)
    email=forms.EmailField(label="Email", required=False)
    barrio=forms.CharField(label="Barrio", max_length=50, min_length=3, required=True)
    dniTutor=forms.IntegerField(label="DNI Tutor",required=True)
    tutor=forms.CharField(label="Tutor", max_length=100, min_length=3, required=True)
    nac=forms.DateField(label="Nacimiento", required=True)
    idPais=forms.Select()
    sexo=forms.Select()
    idObra=forms.Select()
    idLocalidad=forms.Select()
    idEsc=forms.Select()

class frmPorAnio(forms.Form):
    anio = forms.HiddenInput()
