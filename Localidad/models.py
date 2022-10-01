from django.db import models

class Localidad(models.Model):
    idLocalidad=models.IntegerField(primary_key=True)
    localidad=models.CharField(max_length=100)