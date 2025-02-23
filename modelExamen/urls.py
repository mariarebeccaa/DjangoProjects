from django.urls import path
from . import views

urlpatterns = [
    path('elevi/', views.lista_elevi, name='lista_elevi'),
    path('elevi/<int:elev_id>/', views.detalii_elev, name='detalii_elev'),
    path('adauga_elev/', views.adauga_elev, name='adauga_elev'),
]