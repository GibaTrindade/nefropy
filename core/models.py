from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user

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

