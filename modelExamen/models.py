from django.db import models

# Create your models here.

class Elev(models.Model):
    nume = models.CharField(max_length=30)
    prenume = models.CharField(max_length=30)
    data_nasterii = models.DateField()

    def __str__(self):
        return f"{self.nume} {self.prenume}"

class Nota(models.Model):
    valoare = models.IntegerField()
    data_adaugare = models.DateField(auto_now_add=True)
    elev = models.ForeignKey(Elev, on_delete=models.CASCADE)

    def __str__(self):
        return f"Nota {self.valoare} pentru {self.elev}"