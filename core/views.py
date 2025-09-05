# core/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Value, DecimalField
from decimal import Decimal
from django.db.models.functions import Coalesce
from .models import Hospital, Paciente, Producao, ItemProducao, Observacao, Acesso, Conduta
from .forms import ObservacaoForm, AcessoForm, CondutaForm, ProducaoForm, ItemProducaoFormSet
from django.http import HttpResponseBadRequest
from django.utils.dateparse import parse_date
from django.db.models import Prefetch
from django.utils import timezone
from django.db.models import Max
from django.contrib import messages

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
    qs = Producao.objects.select_related("paciente", "paciente__hospital")

    agregados = (
        qs.values("data", "paciente__hospital_id", "paciente__hospital__nome")
          .annotate(
              total=Coalesce(
                  Sum("total_dia"),
                  Value(Decimal("0")),
                  output_field=DecimalField(max_digits=12, decimal_places=2),
              )
          )
          .order_by("-data", "paciente__hospital__nome")
    )

    total_geral = (
        qs.aggregate(
            s=Coalesce(Sum("total_dia"),
                       Value(Decimal("0")),
                       output_field=DecimalField(max_digits=12, decimal_places=2))
        )["s"]
    )

    return render(request, "producao/list.html", {
        "agregados": agregados,
        "total_geral": total_geral,
    })


@login_required
def producao_detalhe(request, data_iso, hospital_id):
    if request.method != "GET":
        return HttpResponseBadRequest("Método inválido")

    data = parse_date(data_iso)
    if not data:
        return HttpResponseBadRequest("Data inválida")

    hospital = get_object_or_404(Hospital, pk=hospital_id)

    producoes = (
        Producao.objects
        .filter(data=data, paciente__hospital=hospital)
        .select_related("paciente")
        .prefetch_related(
            Prefetch(
                "itens",
                queryset=ItemProducao.objects.select_related("procedimento").order_by("procedimento__nome"),
            )
        )
        .order_by("paciente__nome")
    )

    by_paciente = {}
    for p in producoes:
        by_paciente.setdefault(p.paciente, []).append(p)

    # devolve apenas o fragmento com a lista
    return render(request, "producao/_detalhe_fragmento.html", {
        "data": data,
        "hospital": hospital,
        "by_paciente": by_paciente,
    })


@login_required
def evolucao_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)

    last_obs = (Observacao.objects.filter(paciente=paciente)
                .order_by("-criado_em").first())
    last_acesso = (Acesso.objects.filter(paciente=paciente)
                   .order_by("-data_implantacao").first())
    last_conduta = (Conduta.objects.filter(paciente=paciente)
                    .order_by("-criado_em").first())
    hoje = timezone.now().date()
    prod_hoje = (Producao.objects.filter(paciente=paciente, data=hoje)
                 .order_by("-id").first())

    ctx = {
        "paciente": paciente,
        "last_obs": last_obs,
        "last_acesso": last_acesso,
        "last_conduta": last_conduta,
        "prod_hoje": prod_hoje,
        "hoje": hoje,
    }
    return render(request, "evolucao/paciente.html", _cards_context(paciente))

# ---------- Modais HTMX ----------

@login_required
def obs_nova(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    if request.method == "POST":
        form = ObservacaoForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.paciente = paciente
            obj.criado_por = request.user
            obj.save()
            # retorna OOB fragmento para atualizar card
            return render(request, "evolucao/_cards_oob.html",  _cards_context(paciente))
        return render(request, "evolucao/_modal_obs.html", {"form": form, "paciente":paciente}, status=400)
    # GET
    form = ObservacaoForm()
    return render(request, "evolucao/_modal_obs.html", {"form": form, "paciente":paciente})

@login_required
def acesso_novo(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    if request.method == "POST":
        form = AcessoForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.paciente = paciente
            obj.criado_por = request.user
            obj.save()
            return render(request, "evolucao/_cards_oob.html",  _cards_context(paciente))
        return render(request, "evolucao/_modal_acesso.html", {"form": form, "paciente":paciente}, status=400)
    form = AcessoForm()
    return render(request, "evolucao/_modal_acesso.html", {"form": form, "paciente":paciente})

@login_required
def conduta_nova(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    if request.method == "POST":
        form = CondutaForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.paciente = paciente
            obj.criado_por = request.user
            obj.save()
            return render(request, "evolucao/_cards_oob.html",  _cards_context(paciente))
        return render(request, "evolucao/_modal_conduta.html", {"form": form, "paciente":paciente}, status=400)
    form = CondutaForm()
    return render(request, "evolucao/_modal_conduta.html", {"form": form, "paciente":paciente})

@login_required
def producao_nova(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    if request.method == "POST":
        form = ProducaoForm(request.POST)
        formset = ItemProducaoFormSet(request.POST, prefix="itens")
        if form.is_valid() and formset.is_valid():
            prod = form.save(commit=False)
            prod.paciente = paciente
            prod.criado_por = request.user
            prod.save()
            formset.instance = prod
            formset.save()

            # >>> RECARREGA o contexto do card de produção
            hoje = timezone.now().date()
            prod_hoje = (
                Producao.objects
                .filter(paciente=paciente, data=hoje)
                .prefetch_related("itens__procedimento")
                .order_by("-id")
                .first()
            )

            return render(
                request,
                "evolucao/_cards_oob.html",
                 _cards_context(paciente),
            )

        return render(
            request,
            "evolucao/_modal_producao.html",
            {"form": form, "formset": formset, "paciente": paciente},
            status=400,
        )

    # GET
    form = ProducaoForm(initial={"data": timezone.now().date()})
    formset = ItemProducaoFormSet(prefix="itens")
    return render(request, "evolucao/_modal_producao.html", {"form": form, "formset": formset, "paciente": paciente})


def _cards_context(paciente):
    hoje = timezone.now().date()
    return {
        "paciente": paciente,
        "hoje": hoje,
        "last_obs": Observacao.objects.filter(paciente=paciente).order_by("-criado_em").first(),
        "last_acesso": Acesso.objects.filter(paciente=paciente).order_by("-data_implantacao").first(),
        "last_conduta": Conduta.objects.filter(paciente=paciente).order_by("-criado_em").first(),
        "prod_hoje": (
            Producao.objects
            .filter(paciente=paciente, data=hoje)
            .prefetch_related("itens__procedimento")
            .order_by("-id")
            .first()
        ),
    }