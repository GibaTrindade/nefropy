from django.contrib import admin
from django.db.models import Sum, F
from decimal import Decimal
from django.db.models.functions import Coalesce
from django.db.models import Value
from .models import (
    Paciente, Setor, Convenio, Hospital, Observacao,
    Conduta, CondutaDescricao, Acesso, AcessoDescricao,
    Producao, Procedimento, ItemProducao, ProcedimentoValor
)
# Register your models here.
class ObservacaoInline(admin.TabularInline):
    model = Observacao
    extra = 0
    fields = ['descricao', 'criado_por', 'criado_em',]
    #add_fields = ('descricao',)
    list_display = ('descricao', 'criado_por', )
    readonly_fields = ('criado_por','criado_em',)
    ordering = ('-criado_em',)  

class CondutaInline(admin.TabularInline):
    model = Conduta
    extra = 0
    fields = ['descricao', 'criado_por','criado_em', ]
    #add_fields = ('descricao',)
    list_display = ('descricao', 'criado_por', 'criado_em',)
    readonly_fields = ('criado_por','criado_em',)
    ordering = ('-criado_em',)  

class AcessoInline(admin.TabularInline):
    model = Acesso
    extra = 0
    fields = ['nome', 'criado_por','criado_em', 'data_implantacao', 'dias_acesso', ]
    #add_fields = ('descricao',)
    list_display = ('descricao', 'criado_por', 'criado_em', 'data_implantacao', 'dias_acesso',)
    readonly_fields = ('criado_por','criado_em', 'dias_acesso')
    ordering = ('-criado_em',)  

class ItemProducaoInline(admin.TabularInline):
    model = ItemProducao
    extra = 0
    fields = ['procedimento', 'quantidade', 'valor_unitario', 'preview_total']
    readonly_fields = ['preview_total']
    autocomplete_fields = ['procedimento']

    def preview_total(self, obj):
        if not obj.pk:
            return "-"
        total = (obj.valor_unitario or Decimal("0")) * (obj.quantidade or 0)
        return f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    preview_total.short_description = "Total do item"


class ProducaoInline(admin.TabularInline):
    model = Producao
    extra = 0
    fields = ['data', 'total_dia']            # só campos editáveis/derivados visíveis
    readonly_fields = ('total_dia',)          # total_dia é calculado
    ordering = ('-data',)

class PacienteAdmin(admin.ModelAdmin):
    inlines = [CondutaInline, AcessoInline, ObservacaoInline, ProducaoInline,] 
    # Lista de campos que serão exibidos no formulário de edição no admin
    add_fields = ('nome', 'hospital', 'setor', 'numero', 'convenio', 'idade', 'registro', 'diagnostico')
    edit_fields = ('nome','hospital', 'setor', 'numero', 'convenio', 'idade', 'registro', 'diagnostico', 'alta','criado_por')
    list_filter = ('alta', 'hospital',)
    list_display = ('nome','hospital','idade', 'setor', 'numero', 'get_dias_acesso', 'diagnostico', 'get_producao', 'alta',)
    list_editable = ('alta',)
    search_fields = ('nome', 'numero', 'registro', 'hospital__nome', 'convenio__nome')
     # Certifique-se de incluir todos os outros campos do modelo
    readonly_fields = ('criado_por',)
    ordering = ('hospital', 'setor', 'numero',)  

    def get_dias_acesso(self, obj):
        # Consulta relacionada para obter o campo 'dias_acesso' do modelo Acesso
        acessos = Acesso.objects.filter(paciente=obj)
        if acessos.exists():
            return acessos.latest('data_implantacao').dias_acesso
        return None

    get_dias_acesso.short_description = 'Dias de Acesso'

    def get_producao(self, obj):
        total = (Producao.objects
                 .filter(paciente=obj)
                 .aggregate(s=Coalesce(Sum('total_dia'), Value(Decimal("0"))))
                 ['s'])
        # se você preferir mostrar “-” quando for zero, descomente abaixo:
        # if total == 0:
        #     return "-"
        return f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    get_producao.short_description = 'Produção'
    
    def get_fields(self, request, obj=None):
        # Se estiver criando um novo paciente, use os campos de criação
        if not obj:
            return self.add_fields
        # Caso contrário, use os campos de edição
        return self.edit_fields

    def save_model(self, request, obj, form, change):
        # Defina o campo 'criado_por' como o usuário atual
        if not change:  # Isso garante que o campo só será definido ao criar um novo registro
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)
    
    def save_formset(self, request, form, formset, change): 
        if formset.model == Observacao:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.criado_por = request.user
                instance.save()
        elif formset.model == Conduta:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.criado_por = request.user
                instance.save()
        elif formset.model == Acesso:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.criado_por = request.user
                instance.save()
        elif formset.model == Producao:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.criado_por = request.user
                instance.save()
        else:
            formset.save()


class SetorAdmin(admin.ModelAdmin):
    add_fields = ('nome',)
    edit_fields = ('nome', 'criado_por',)     
    
    readonly_fields = ('criado_por',)    

    def get_fields(self, request, obj=None):
        # Se estiver criando um novo paciente, use os campos de criação
        if not obj:
            return self.add_fields
        # Caso contrário, use os campos de edição
        return self.edit_fields
      
    def save_model(self, request, obj, form, change):
        # Defina o campo 'criado_por' como o usuário atual
        if not change:  # Isso garante que o campo só será definido ao criar um novo registro
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)

class ConvenioAdmin(admin.ModelAdmin):
    add_fields = ('nome',)
    edit_fields = ('nome', 'criado_por',)     
    search_fields = ('nome',)
    readonly_fields = ('criado_por',)    

    def get_fields(self, request, obj=None):
        # Se estiver criando um novo paciente, use os campos de criação
        if not obj:
            return self.add_fields
        # Caso contrário, use os campos de edição
        return self.edit_fields
      
    def save_model(self, request, obj, form, change):
        # Defina o campo 'criado_por' como o usuário atual
        if not change:  # Isso garante que o campo só será definido ao criar um novo registro
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)

class HospitalAdmin(admin.ModelAdmin):
    add_fields = ('nome','valor_parecer', 'valor_hemodialise', 'valor_hdfc', 'valor_cateter',)
    edit_fields = ('nome', 'valor_parecer', 'valor_hemodialise', 'valor_hdfc', 'valor_cateter', 'criado_por',)     
    search_fields = ('nome',)
    readonly_fields = ('criado_por',)    

    def get_fields(self, request, obj=None):
        # Se estiver criando um novo paciente, use os campos de criação
        if not obj:
            return self.add_fields
        # Caso contrário, use os campos de edição
        return self.edit_fields
      
    def save_model(self, request, obj, form, change):
        # Defina o campo 'criado_por' como o usuário atual
        if not change:  # Isso garante que o campo só será definido ao criar um novo registro
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)



class ObservacaoAdmin(admin.ModelAdmin):
    add_fields = ('descricao', 'paciente',)
    edit_fields = ('descricao', 'paciente', 'criado_por',)     
    list_display = ('descricao', 'criado_em', 'criado_por')
    readonly_fields = ('criado_por',)  
    ordering = ('-criado_em', 'criado_por')  

    def get_fields(self, request, obj=None):
        # Se estiver criando um novo paciente, use os campos de criação
        if not obj:
            return self.add_fields
        # Caso contrário, use os campos de edição
        return self.edit_fields
    def save_model(self, request, obj, form, change):
        # Defina o campo 'criado_por' como o usuário atual
        if not change:  # Isso garante que o campo só será definido ao criar um novo registro
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)
      
class CondutaAdmin(admin.ModelAdmin):
    add_fields = ('descricao', 'paciente',)
    edit_fields = ('descricao', 'paciente', 'criado_por',)     
    
    readonly_fields = ('criado_por',)    

    def get_fields(self, request, obj=None):
        # Se estiver criando um novo paciente, use os campos de criação
        if not obj:
            return self.add_fields
        # Caso contrário, use os campos de edição
        return self.edit_fields
    def save_model(self, request, obj, form, change):
        # Defina o campo 'criado_por' como o usuário atual
        if not change:  # Isso garante que o campo só será definido ao criar um novo registro
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)

class AcessoAdmin(admin.ModelAdmin):
    add_fields = ('nome', 'paciente', 'data_implantacao')
    edit_fields = ('nome', 'paciente', 'data_implantacao','criado_por',)     
    
    readonly_fields = ('criado_por', 'dias_acesso')    

    def get_fields(self, request, obj=None):
        # Se estiver criando um novo paciente, use os campos de criação
        if not obj:
            return self.add_fields
        # Caso contrário, use os campos de edição
        return self.edit_fields
    def save_model(self, request, obj, form, change):
        # Defina o campo 'criado_por' como o usuário atual
        if not change:  # Isso garante que o campo só será definido ao criar um novo registro
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)

class ProducaoAdmin(admin.ModelAdmin):
    inlines = [ItemProducaoInline]
    # novos campos (sem os booleans/inteiros antigos)
    add_fields = ('paciente', 'data', 'criado_por')
    edit_fields = ('paciente', 'data', 'total_dia', 'criado_por')
    readonly_fields = ('criado_por', 'total_dia')
    list_display = ('paciente', 'data', 'paciente_hospital', 'total_dia_fmt', 'criado_por')
    list_filter = ('paciente__hospital', 'data')
    search_fields = ('paciente__nome',)
    ordering = ('-data', '-id')
    date_hierarchy = 'data'
    autocomplete_fields = ['paciente']

    def paciente_hospital(self, obj):
        return getattr(getattr(obj.paciente, 'hospital', None), 'nome', '-')
    paciente_hospital.short_description = 'Hospital'

    def total_dia_fmt(self, obj):
        if obj.total_dia is None:
            return "-"
        return f"R$ {obj.total_dia:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    total_dia_fmt.short_description = 'Total do dia'

    def get_fields(self, request, obj=None):
        return self.add_fields if not obj else self.edit_fields

    def save_model(self, request, obj, form, change):
        if not change and getattr(obj, "criado_por_id", None) is None:
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)

    # ação opcional para recomputar totais se você editar itens via shell/import
    @admin.action(description="Recomputar total do dia")
    def recomputar_total_dia(self, request, queryset):
        for p in queryset:
            p.recomputar_total(save=True)

@admin.register(Procedimento)
class ProcedimentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'ativo', 'codigo', 'unidade')
    list_filter = ('ativo', 'tipo')
    search_fields = ('nome', 'codigo')

# ----------------------------
# ProcedimentoValor (tarifas)
# ----------------------------
@admin.register(ProcedimentoValor)
class ProcedimentoValorAdmin(admin.ModelAdmin):
    list_display = ('procedimento', 'hospital', 'convenio', 'valor', 'vigencia_inicio', 'vigencia_fim')
    list_filter = ('hospital', 'convenio', 'procedimento')
    search_fields = ('procedimento__nome', 'hospital__nome', 'convenio__nome')
    autocomplete_fields = ['procedimento', 'hospital', 'convenio']
    ordering = ('procedimento', 'hospital', '-vigencia_inicio')


admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Setor, SetorAdmin)
admin.site.register(Convenio, ConvenioAdmin)
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Observacao, ObservacaoAdmin)
admin.site.register(Conduta, CondutaAdmin)
admin.site.register(CondutaDescricao)
admin.site.register(Acesso, AcessoAdmin)
admin.site.register(AcessoDescricao)
admin.site.register(Producao, ProducaoAdmin)