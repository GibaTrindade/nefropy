from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.utils import timezone

# Create your models here.
class Setor(models.Model):
    nome = models.CharField(max_length=20, blank=False, null=False)
    criado_em = models.DateField(auto_now_add=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return self.nome
    
class Convenio(models.Model):
    nome = models.CharField(max_length=20, blank=False, null=False)
    criado_em = models.DateField(auto_now_add=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return self.nome

class Hospital(models.Model):
    nome = models.CharField(max_length=20, blank=False, null=False)
    valor_parecer = models.FloatField(default=0)
    valor_hemodialise = models.FloatField(default=0)
    valor_hdfc = models.FloatField(default=0)
    valor_cateter = models.IntegerField(default=0)
    criado_em = models.DateField(auto_now_add=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return self.nome


class Paciente(models.Model):
    nome =  models.CharField(max_length=400, blank=False, null=False)
    setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, null=True,blank=True)
    numero = models.CharField(max_length=400, blank=True, null=True)
    idade = models.IntegerField(blank=True, null=True)
    registro = models.CharField(blank=True, null=True)
    diagnostico = models.TextField(max_length=400, default='', blank=True, null=True)
    alta = models.BooleanField(default=False)
    convenio = models.ForeignKey(Convenio, on_delete=models.SET_NULL, null=True,blank=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True,blank=True)
    
    criado_em = models.DateField(auto_now_add=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)

    #convenio = models.CharField(blank=True, null=True)
    #conduta = models.CharField(max_length=400, default='')
    #producao = models.CharField(max_length=400, blank=False, null=False)
    #acesso = models.ForeignKey(User, on_delete=models.SET_NULL)
    #history = HistoricalRecords()
    
    def __str__(self):
        return '(' + self.hospital.nome +')'+self.nome

class AcessoDescricao(models.Model):
    descricao = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return self.descricao

class Acesso(models.Model):
    nome = models.ForeignKey(AcessoDescricao,on_delete=models.SET_NULL, blank=False, null=True)
    data_implantacao = models.DateField()
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True,blank=True)
    dias_acesso = models.IntegerField(blank=True, null=True)
    criado_em = models.DateField(auto_now_add=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)

    
    def __str__(self):
        return self.nome.descricao

    def save(self, *args, **kwargs):
        # Calcula a diferença em dias entre a data de implantação e a data de hoje
        if self.data_implantacao:
            hoje = timezone.now().date()
            diferenca = hoje - self.data_implantacao
            self.dias_acesso = diferenca.days
        super(Acesso, self).save(*args, **kwargs)
    

class Observacao(models.Model):
    descricao = models.TextField(max_length=4000, blank=False, null=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True,blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return self.descricao

class CondutaDescricao(models.Model):
    descricao = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.descricao

class Conduta(models.Model):
    descricao = models.ForeignKey(CondutaDescricao, on_delete=models.CASCADE, blank=False, null=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True,blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return self.descricao.descricao

class Procedimento(models.Model):
    nome = models.CharField(max_length=100, blank=False, null=False)
    valor = models.FloatField(blank=False, null=False)

    def __str__(self):
        return self.nome

class Producao(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.DO_NOTHING)
    #procedimento = models.ManyToManyField(Procedimento)
    parecer_visita = models.BooleanField(default=False)
    hemodialise = models.BooleanField(default=False)
    hdfc = models.BooleanField(default=False)
    cateter = models.IntegerField(default=0)
    criado_em = models.DateField()
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)
    total_dia = models.FloatField(blank=True, null=True)

    
    def save(self, *args, **kwargs):
        # Calcula a diferença em dias entre a data de implantação e a data de hoje
        total = 0
        if self.parecer_visita:
            total += self.paciente.hospital.valor_parecer
        if self.hemodialise:
            total += self.paciente.hospital.valor_hemodialise
        if self.hdfc:
            total += self.paciente.hospital.valor_hdfc
        self.total_dia = total + (self.paciente.hospital.valor_cateter * self.cateter)
        super(Producao, self).save(*args, **kwargs)

    def __str__(self):
        return self.paciente.nome