from django.db import models

# Create your models here.

class Marca(models.Model):
    nume = models.CharField(max_length=50)  # Numele brandului
    tara_origine = models.CharField(max_length=50, blank=True, null=True)  # Țara de origine

    def __str__(self):
        return self.nume

class Categorie(models.Model):
    nume = models.CharField(max_length=50)  # Numele categoriei (ex: Ruj)
    descriere = models.TextField(blank=True, null=True)  # Descriere opțională

    def __str__(self):
        return self.nume

class Produs(models.Model):
    nume = models.CharField(max_length=100)  # Numele produsului
    pret = models.DecimalField(max_digits=10, decimal_places=2)  # Prețul produsului
    descriere = models.TextField(blank=True, null=True)  # Descrierea produsului
    marci = models.ManyToManyField(Marca, related_name="produse")  # Relația many-to-many cu Marca
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, related_name="produse")  # Relația one-to-many cu Categorie

    def __str__(self):
        return self.nume

class Recenzie(models.Model):
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE, related_name="recenzii")  # Legătura către Produs
    continut = models.TextField()  # Conținutul recenziei
    rating = models.IntegerField()  # Rating pentru recenzie, ex: 1-5

    def __str__(self):
        return f"Recenzie pentru {self.produs.nume} - Rating: {self.rating}"

class Favorite(models.Model):
    produse = models.ManyToManyField(Produs, related_name="favorit")  # Relația many-to-many cu Produs

    def __str__(self):
        return "Lista de favorite"

# Lab6
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    telefon = models.CharField(max_length=15, blank=True, null=True)
    data_nasterii = models.DateField(blank=True, null=True)
    oras = models.CharField(max_length=100, blank=True, null=True)
    ocupatie = models.CharField(max_length=100, blank=True, null=True)
    descriere = models.TextField(blank=True, null=True)
    cod = models.CharField(max_length=100, blank=True, null=True)
    email_confirmat = models.BooleanField(default=False)
    def generate_confirmation_code(self):
        self.cod = str(uuid.uuid4())[:16] # cod unic de 16 caractere
        self.save()
        
#Lab7
# models.py
from django.db import models
from django.core.validators import MinValueValidator

class Vizualizari(models.Model):
    """
    Model pentru urmărirea ultimelor N produse vizualizate de către utilizatori.
    """
    utilizator = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    produs = models.ForeignKey('Produs', on_delete=models.CASCADE)
    data_vizualizare = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_vizualizare']  # Ordonare descrescătoare după dată

    def save(self, *args, **kwargs):
        # Logica pentru menținerea doar a ultimelor N vizualizări per utilizator
        if not self.pk:  # Doar pentru înregistrări noi
            N = 5  # Numărul maxim de vizualizări per utilizator
            vizualizari_utilizator = Vizualizari.objects.filter(
                utilizator=self.utilizator
            )
            if vizualizari_utilizator.count() >= N:
                # Șterge cea mai veche vizualizare
                vizualizari_utilizator.last().delete()
        super().save(*args, **kwargs)

class Promotie(models.Model):
    """
    Model pentru stocarea promoțiilor și detaliilor acestora.
    """
    nume = models.CharField(max_length=100)
    data_creare = models.DateTimeField(auto_now_add=True)
    data_expirare = models.DateTimeField()
    discount = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    categorii = models.ManyToManyField('Categorie')  # Legătura cu categoriile
    descriere = models.TextField()  # Câmp pentru descrierea promoției

    def __str__(self):
        return f"{self.nume} ({self.discount}% până la {self.data_expirare})"

# Lab8
