from django.db import models

class Pais(models.Model):
    idPais=models.IntegerField(primary_key=True)
    pais=models.CharField(max_length=100)