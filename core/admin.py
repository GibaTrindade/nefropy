from django.contrib import admin

from .models import Paciente, Setor, Convenio, Hospital, Observacao, Conduta, CondutaDescricao
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

class PacienteAdmin(admin.ModelAdmin):
    inlines = [ ObservacaoInline, CondutaInline ]
    # Lista de campos que serão exibidos no formulário de edição no admin
    add_fields = ('nome', 'hospital', 'setor', 'numero', 'convenio', 'idade', 'registro', 'diagnostico')
    edit_fields = ('nome','hospital', 'setor', 'numero', 'convenio', 'idade', 'registro', 'diagnostico', 'alta','criado_por')
    list_filter = ('alta', 'hospital',)
    list_display = ('nome','hospital','idade', 'setor', 'numero', 'diagnostico', 'alta',)
    list_editable = ('alta',)
     # Certifique-se de incluir todos os outros campos do modelo
    readonly_fields = ('criado_por',)
    ordering = ('hospital__nome', 'setor', 'numero',)  

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



class ObservacaoAdmin(admin.ModelAdmin):
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


admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Setor, SetorAdmin)
admin.site.register(Convenio, ConvenioAdmin)
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Observacao, ObservacaoAdmin)
admin.site.register(Conduta, CondutaAdmin)
admin.site.register(CondutaDescricao)