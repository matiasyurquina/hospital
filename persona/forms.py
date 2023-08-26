from django import forms
from .models import *

class FormNewPerson(forms.ModelForm):
    nombre=forms.CharField(label="Nombre", max_length=100, min_length=2, required=True)
    apellido=forms.CharField(label="Apellido", max_length=100, min_length=2, required=True)
    dni=forms.IntegerField(label="DNI", required=True)
    cel=forms.IntegerField(label="Celular", required=False)
    dir=forms.CharField(label="Dirección", max_length=100, min_length=3, required=True)
    email=forms.EmailField(label="Email", required=False)
    barrio=forms.CharField(label="Barrio", max_length=50, min_length=3, required=True)
    dniTutor=forms.IntegerField(label="DNI Tutor",required=True)
    pmot=forms.CharField(label="Tutor", max_length=100, min_length=3, required=True)
    nac=forms.DateField(label="Nacimiento", required=True)
    sexo=forms.Select()
    idPais=forms.Select()
    idObra=forms.Select()
    idLocalidad=forms.Select()
    idEsc=forms.Select()

    # class Meta:
    #     model = Persona
    #     fields = ['nombre', 'apellido', 'dni', 'cel', 'dir', 'email', 'barrio', 'dniTutor', 'pmot', 'nac', 'sexo', 'idPais', 'idObra', 'idLocalidad', 'idEsc']
        # widgets = {
        #     'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        #     'apellido': forms.TextInput(attrs={'class': 'form-control'}),
        # }


class frmPorAnio(forms.Form):
    anio = forms.HiddenInput()
