from datetime import date
from django.db import models
from Escuela.models import Escuela
from Localidad.models import Localidad
from obraSocial.models import ObraSocial
from Pais.models import Pais
import random

class Persona(models.Model):
    idPersona=models.IntegerField(primary_key=True)
    nombre=models.CharField(max_length=100)
    apellido=models.CharField(max_length=100)
    dni=models.IntegerField(unique=True)    
    sexo=models.BooleanField()
    nac=models.DateField()
    email=models.EmailField(blank=True, null=True)
    cel=models.BigIntegerField(blank=True, null=True)
    calle=models.CharField(max_length=100)
    barrio=models.CharField(max_length=50)
    pmot=models.CharField(max_length=100)
    dniTutor=models.IntegerField()
    idPais=models.ForeignKey(Pais, on_delete=models.CASCADE)
    idLocalidad=models.ForeignKey(Localidad, on_delete=models.CASCADE)
    idEsc=models.ForeignKey(Escuela, on_delete=models.CASCADE)
    idObra=models.ForeignKey(ObraSocial, on_delete=models.CASCADE)
    fecha_registro=models.DateField(auto_now=True, null=False)

    class Meta:
        ordering = ['apellido', 'nombre']

class Activator(models.Model):
    activation_code = models.CharField(max_length=254, null=True)
    activation_code_encoded = models.CharField(max_length=254, null=True)
    activated = models.BooleanField(default=False, null=False)
