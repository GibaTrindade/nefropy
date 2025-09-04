from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("hospitais/", views.hospitais_list, name="hospitais_list"),
    path("pacientes/", views.pacientes_list, name="pacientes_list"),
    path("producao/", views.producao_list, name="producao_list"),
]
