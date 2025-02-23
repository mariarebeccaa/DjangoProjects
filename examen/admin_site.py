from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Client, Comanda
# Register your models here.

class ExamenAdminSite(AdminSite):
    site_header = 'Examen Admin'
    site_title = 'Examen Admin Portal'
    index_title = 'Welcome to Examen Admin'
    
examen_admin_site = ExamenAdminSite(name='examen_admin')

examen_admin_site.register(Client)
examen_admin_site.register(Comanda)