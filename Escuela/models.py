from django.db import models

class Escuela(models.Model):
    idEsc=models.IntegerField(primary_key=True)
    escuela=models.CharField(max_length=100, unique=True)
