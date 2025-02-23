from django.urls import path
from . import views

urlpatterns = [
        path("afis_template", views.afis_template, name="afis_template"),
        path('lista_produse/', views.lista_produse, name="lista_produse"),
        # path('mesaj_trimis/', views.mesaj_trimis, name='mesaj_trimis'),
        path('contact/', views.contact_view, name='contact'),
        path('filtreaza_produse/', views.filtreaza_produse, name='filtreaza_produse'),
        path('lista_mesaje/', views.lista_mesaje, name='lista_mesaje'),
        path('adauga_produs/', views.adauga_produs, name='adauga_produs'),
        path('inregistrare/', views.register_view, name='inregistrare'),
        path('login/', views.custom_login_view, name='login'),
        path('change-password/', views.change_password_view, name='change-password'),
        path('logout/', views.logout_view, name='logout'),
        path('profile/', views.profile_view, name='profile'),
        path("", views.index, name="index"),
        path('confirma_mail/<str:cod>/', views.confirma_mail, name='confirma_mail'),
        path('promotii/', views.creeaza_promotie, name='promotii'),
        path('promotii/lista/', views.lista_promotii, name='lista_promotii'),
        path('produs/<int:produs_id>/vizualizare/', views.urmareste_vizualizare, name='urmareste_vizualizare'),
        path('produs/<int:produs_id>/', views.detalii_produs, name='detalii_produs'),
        path('test_403/', views.test_403_view, name='test_403'),
]