# core/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Observacao, Acesso, Conduta, Producao, ItemProducao, CondutaDescricao, AcessoDescricao
from django.utils import timezone

class ObservacaoForm(forms.ModelForm):
    class Meta:
        model = Observacao
        fields = ["descricao"]
        widgets = {"descricao": forms.Textarea(attrs={"class":"form-control","rows":6,"placeholder":"Evolução / conduta..."})}

class AcessoForm(forms.ModelForm):
    class Meta:
        model = Acesso
        fields = ["nome","data_implantacao"]
        widgets = {
            "nome": forms.Select(attrs={"class":"form-select"}),
            "data_implantacao": forms.DateInput(attrs={"type":"date","class":"form-control"}),
        }

class CondutaForm(forms.ModelForm):
    class Meta:
        model = Conduta
        fields = ["descricao"]
        widgets = {"descricao": forms.Select(attrs={"class":"form-select"})}

# Produção do dia + itens (procedimento/quantidade/valor)
class ProducaoForm(forms.ModelForm):
    class Meta:
        model = Producao
        fields = ["data"]  # e.g., seu campo é 'data'
        widgets = {"data": forms.DateInput(attrs={"type":"date","class":"form-control", "value": timezone.now().date()})}

class ItemProducaoForm(forms.ModelForm):
    class Meta:
        model = ItemProducao
        fields = ["procedimento", "quantidade"]
        widgets = {
            "procedimento": forms.Select(attrs={"class":"form-select"}),
            "quantidade": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
        }

ItemProducaoFormSet = inlineformset_factory(
    Producao, ItemProducao, form=ItemProducaoForm, extra=1, can_delete=True
)
