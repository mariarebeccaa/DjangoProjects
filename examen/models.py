from django.db import models

class Client(models.Model):
    nume = models.CharField(max_length=30)
    prenume = models.CharField(max_length=30)
    email = models.EmailField()
    data_nasterii = models.DateField()

    def __str__(self):
        return f"{self.nume} {self.prenume}"

class Comanda(models.Model):
    produs = models.CharField(max_length=100)
    pret = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comanda pentru {self.produs} - {self.client}"