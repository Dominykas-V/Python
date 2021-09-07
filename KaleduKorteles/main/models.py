#from typing_extensions import Required
from django.db import models
from datetime import date

class Zmogus(models.Model):
    vardas = models.CharField(max_length=250)
    last_login = models.DateField(default=date.today)
    pora = models.CharField(max_length=250, blank=True, default="________")
    arPanaudotas = models.BooleanField(default=False, blank=True)
    admin = models.BooleanField(default=False)


    def __str__(self):
        return self.vardas
