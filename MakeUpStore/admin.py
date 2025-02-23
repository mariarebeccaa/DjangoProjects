from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import CustomUser, Marca, Categorie, Produs, Recenzie, Favorite

# Register your models here.
from .models import Marca, Categorie, Produs, Recenzie, Favorite

# practic aici adaug modelele in panoul de administrare
# in acest fel voi avea o interfata pt adaugarea, modificarea si stergerea inreg in fiecare tabel

# admin.site.register(Marca)
# admin.site.register(Categorie)
# # admin.site.register(Produs)
# admin.site.register(Recenzie)
admin.site.register(Favorite)

class ProdusAdmin(admin.ModelAdmin):
    fields = ['pret', 'nume', 'descriere', 'categorie']  # Schimba ordinea campurilor
    search_fields = ['nume'] #camp de cautare dupa nume
    list_filter = ['categorie', 'nume', 'pret', 'marci']

class MarcaAdmin(admin.ModelAdmin):
    search_fields = ['nume'] 

class CategorieAdmin(admin.ModelAdmin):
    search_fields = ['nume']  

class RecenzieAdmin(admin.ModelAdmin):
    search_fields = ['rating'] 
    fieldsets = (
        ('Asocieri', {
            'fields': ['produs']
        }),
        ('Detalii', {
            'fields': ('rating', 'continut')
        }),
    )

admin.site.register(Produs, ProdusAdmin)
admin.site.register(Marca, MarcaAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Recenzie, RecenzieAdmin)

# Personalizare titlu si header pt Admin
admin.site.site_header = "Panoul de Administrare MakeUp Store"
admin.site.site_title = "MakeUp Store Admin"
admin.site.index_title = "Bine ați venit în Panoul de Administrare"

# Register CustomUser model
admin.site.register(CustomUser)

# Create the group and assign permissions
product_content_type = ContentType.objects.get_for_model(Produs)
permissions = Permission.objects.filter(content_type=product_content_type)
administratori_produse, created = Group.objects.get_or_create(name='Administratori_produse')
administratori_produse.permissions.set(permissions)

# Add a user to the group
user = CustomUser.objects.get(username='mariarebecca')  # Replace with the actual username
user.groups.add(administratori_produse)

