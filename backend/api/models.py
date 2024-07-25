from django.db import models


# Create your models here.
class Conglomerate(models.Model):
    name = models.TextField(blank=False)


class Company(models.Model):
    name = models.TextField(blank=False)
    conglomerado = models.ForeignKey(Conglomerate, on_delete=models.CASCADE)


class Store(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # campos bsale
    name = models.TextField()
    bsaleId = models.IntegerChoices(blank=False)
    descripcion = models.TextField()
    direccion = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    isVirtual = models.BooleanField()
    country = models.TextField()
    municipality = models.TextField()
    city = models.TextField()
    zipCode = models.TextField()
    costCenter = models.TextField()
    state = models.BooleanField()
