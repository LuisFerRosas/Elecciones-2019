from django.db import models
from django.db.models import Sum
# Create your models here.

class Pais(models.Model):
    nombre=models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.nombre
    
class Departamento(models.Model):
    numero=models.IntegerField(unique=True)
    nombre=models.CharField(max_length=50)
    #related fields 
    pais=models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='departamentos')

    def __str__(self):
        return self.nombre

class Municipio(models.Model):
    nombre=models.CharField(max_length=150, unique=True)
    #related fields
    departamento=models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='municipios')

    def __str__(self):
        return self.nombre

class Recinto(models.Model):
    nombre=models.CharField(max_length=150, unique=True)
    #related fields
    municipio=models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='recintos')

    def __str__(self):
        return self.nombre

class Mesa(models.Model):
    numero=models.IntegerField(unique=True)
    codigo=models.CharField(max_length=150, unique=True)
    inscritos=models.IntegerField()
    cc=models.IntegerField(default=0)
    fpv=models.IntegerField(default=0)
    mts=models.IntegerField(default=0)
    ucs=models.IntegerField(default=0)
    mas=models.IntegerField(default=0)
    v1f=models.IntegerField(default=0)
    pdc=models.IntegerField(default=0)
    mnr=models.IntegerField(default=0)
    panbol=models.IntegerField(default=0)
    validos=models.IntegerField(default=0)
    blancos=models.IntegerField(default=0)
    nulos=models.IntegerField(default=0)
    trep=models.BooleanField()
    #related fields
    recinto=models.ForeignKey(Recinto, on_delete=models.CASCADE, related_name='mesas')

    def __str__(self):
        return str(self.numero)