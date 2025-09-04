# core/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum
from .models import Hospital, Paciente, Producao

@login_required
def home(request):
    ctx = {
        "total_hospitais": Hospital.objects.count(),
        "total_pacientes": Paciente.objects.count(),
        "total_producao": Producao.objects.aggregate(s=Sum("total_dia"))["s"] or 0,
    }
    return render(request, "home.html", ctx)

@login_required
def hospitais_list(request):
    hospitais = Hospital.objects.all().order_by("nome")
    return render(request, "hospitais/list.html", {"hospitais": hospitais})

@login_required
def pacientes_list(request):
    q = request.GET.get("q", "").strip()
    qs = Paciente.objects.select_related("hospital")
    if q:
        qs = qs.filter(nome__icontains=q)
    return render(request, "pacientes/list.html", {"pacientes": qs, "q": q})

@login_required
def producao_list(request):
    producoes = (Producao.objects
                 .select_related("paciente", "paciente__hospital")
                 .order_by("-data", "-id")[:50])
    return render(request, "producao/list.html", {"producoes": producoes})
