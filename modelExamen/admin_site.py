from django.contrib.admin import AdminSite
from .models import Elev, Nota
from django.contrib import admin

class ModelExamenAdminSite(AdminSite):
    site_header = 'Model Examen Admin'
    site_title = 'Model Examen Admin Portal'
    index_title = 'Welcome to Model Examen Admin'

model_examen_admin_site = ModelExamenAdminSite(name='model_examen_admin')

# Register your models here
model_examen_admin_site.register(Elev)
model_examen_admin_site.register(Nota)