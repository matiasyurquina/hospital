from django.db import models

class ObraSocial(models.Model):
    idOsocial=models.IntegerField(primary_key=True)
    obraSocial=models.CharField(max_length=150, unique=True)