from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("hospitais/", views.hospitais_list, name="hospitais_list"),
    path("pacientes/", views.pacientes_list, name="pacientes_list"),
    path("producao/", views.producao_list, name="producao_list"),
    # detalhe HTMX: data no formato YYYY-MM-DD
    path("producao/detalhe/<slug:data_iso>/<int:hospital_id>/", views.producao_detalhe, name="producao_detalhe"),
    path("pacientes/<int:paciente_id>/evolucao/", views.evolucao_paciente, name="evolucao_paciente"),

    # modais HTMX
    path("pacientes/<int:paciente_id>/observacao/nova/", views.obs_nova, name="obs_nova"),
    path("pacientes/<int:paciente_id>/acesso/nova/",     views.acesso_novo, name="acesso_novo"),
    path("pacientes/<int:paciente_id>/conduta/nova/",    views.conduta_nova, name="conduta_nova"),
    path("pacientes/<int:paciente_id>/producao/nova/",   views.producao_nova, name="producao_nova"),
]
