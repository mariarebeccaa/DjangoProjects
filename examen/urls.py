from django.urls import path
from . import views

urlpatterns = [
    path('clienti/', views.lista_clienti, name='lista_clienti'),
    path('clienti/<int:client_id>/', views.detalii_comanda, name='detalii_comanda'),
    path('adauga_comanda/', views.adauga_comanda, name='adauga_comanda'),
]