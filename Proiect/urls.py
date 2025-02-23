"""
URL configuration for Proiect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from modelExamen.admin_site import model_examen_admin_site

from examen.admin_site import examen_admin_site




urlpatterns = [
    path('', include('aplicatie_1.urls')),
    path('proiect/', include('MakeUpStore.urls')),
    path('admin/', admin.site.urls),
    path('modelExamen/admin/', model_examen_admin_site.urls),  # Custom admin site for modelExamen
    path('modelExamen/', include('modelExamen.urls')),
    path('examen/admin/', examen_admin_site.urls),  
    path('examen/', include('examen.urls')),
]
from MakeUpStore import views 
handler403 = views.custom_403_view

