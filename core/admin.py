from django.contrib import admin

from .models import Paciente, Setor, Convenio, Hospital, Observacao, \
Conduta, CondutaDescricao, Acesso, AcessoDescricao, Producao, Procedimento
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

class ProducaoInline(admin.TabularInline):
    model = Producao
    extra = 0
    fields = ['parecer_visita','hemodialise', 'hdfc', 'cateter', 'criado_em', 'criado_por']
    #add_fields = ('descricao',)
    list_display = ('paciente', 'parecer_visita', 'hemodialise', 'hdfc', 'cateter', 'criado_em', 'criado_por',)
    readonly_fields = ('criado_por',)
    ordering = ('-criado_em',)  

class PacienteAdmin(admin.ModelAdmin):
    inlines = [CondutaInline, AcessoInline, ObservacaoInline, ProducaoInline,] 
    # Lista de campos que serão exibidos no formulário de edição no admin
    add_fields = ('nome', 'hospital', 'setor', 'numero', 'convenio', 'idade', 'registro', 'diagnostico')
    edit_fields = ('nome','hospital', 'setor', 'numero', 'convenio', 'idade', 'registro', 'diagnostico', 'alta','criado_por')
    list_filter = ('alta', 'hospital',)
    list_display = ('nome','hospital','idade', 'setor', 'numero', 'get_dias_acesso', 'diagnostico', 'get_producao', 'alta',)
    list_editable = ('alta',)
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
        # Consulta relacionada para obter o campo 'dias_acesso' do modelo Acesso
        total_prod=0
        producoes = Producao.objects.filter(paciente=obj)
        if producoes.exists():
            for producao in producoes:
                total_prod += producao.total_dia
            return total_prod #acessos.latest('-criado_em').total_dia
        return None

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
    add_fields = ('paciente',  'parecer_visita','hemodialise', 'hdfc', 'cateter', 'criado_em', 'criado_por',)
    edit_fields = ('paciente',  'parecer_visita','hemodialise', 'hdfc', 'cateter', 'criado_em') 
    list_display = ('paciente',  'parecer_visita', 'hemodialise', 'hdfc', 'cateter', 'criado_em', 'criado_por', 'total_dia')    
    list_editable = ('parecer_visita', 'hemodialise', 'hdfc', 'cateter', 'criado_em')
    list_filter = ( 'paciente__hospital', 'criado_em')
    readonly_fields = ('criado_por', )  
    ordering = ('paciente',)

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
admin.site.register(Procedimento)