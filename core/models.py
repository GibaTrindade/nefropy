from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal

# Create your models here.

class Procedimento(models.Model):
    TIPO_BOOLEANO = "bool"
    TIPO_INTEIRO = "int"
    TIPO_CHOICES = [
        (TIPO_BOOLEANO, "Booleano (0/1)"),
        (TIPO_INTEIRO, "Inteiro (quantidade)"),
    ]

    nome = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=8, choices=TIPO_CHOICES, default=TIPO_BOOLEANO)
    ativo = models.BooleanField(default=True)

    # (opcional) códigos de tabela, unidade de medida, etc.
    codigo = models.CharField(max_length=50, blank=True, null=True)
    unidade = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nome
    

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


class ProcedimentoValor(models.Model):
    procedimento = models.ForeignKey(Procedimento, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    convenio = models.ForeignKey(Convenio, on_delete=models.SET_NULL, null=True, blank=True)
    valor = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    vigencia_inicio = models.DateField()
    vigencia_fim = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("procedimento", "hospital", "convenio", "vigencia_inicio")

    def __str__(self):
        conv = self.convenio.nome if self.convenio else "Todos convênios"
        fim = self.vigencia_fim or "sem fim"
        return f"{self.procedimento} @ {self.hospital} / {conv} ({self.vigencia_inicio} → {fim})"

    @classmethod
    def valor_em(cls, procedimento, hospital, convenio, data):
        """
        Recupera o preço vigente na data.
        Regra: (vigencia_inicio <= data) & (vigencia_fim is null or data <= vigencia_fim)
        Se não houver tarifa específica do convênio, tenta 'convenio=None'.
        """
        qs = cls.objects.filter(
            procedimento=procedimento, hospital=hospital,
            vigencia_inicio__lte=data
        ).filter(models.Q(vigencia_fim__isnull=True) | models.Q(vigencia_fim__gte=data))
        if convenio:
            pv = qs.filter(convenio=convenio).order_by("-vigencia_inicio").first()
            if pv:
                return pv.valor
        pv_generic = qs.filter(convenio__isnull=True).order_by("-vigencia_inicio").first()
        return pv_generic.valor if pv_generic else Decimal("0.00")
    
# class Procedimento(models.Model):
#     nome = models.CharField(max_length=100, blank=False, null=False)
#     valor = models.FloatField(blank=False, null=False)

#     def __str__(self):
#         return self.nome

class Producao(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.DO_NOTHING, related_name="producoes")
    data = models.DateField(default=timezone.now)
    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total_dia = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ("paciente", "data")  # 1 registro agregado por dia/paciente (opcional)
        ordering = ["-data", "-id"]

    def __str__(self):
        return f"Produção {self.paciente} em {self.data}"

    def recomputar_total(self, save=True):
        total = self.itens.aggregate(s=models.Sum(models.F("quantidade") * models.F("valor_unitario")))["s"] or Decimal("0")
        self.total_dia = total
        if save:
            self.save(update_fields=["total_dia"])
        return total


class ItemProducao(models.Model):
    producao = models.ForeignKey(Producao, on_delete=models.CASCADE, related_name="itens")
    procedimento = models.ForeignKey(Procedimento, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1, validators=[MinValueValidator(0)])
    # Snapshot do valor unitário vigente na data da produção
    valor_unitario = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])

    class Meta:
        unique_together = ("producao", "procedimento")  # evita duplicar o mesmo procedimento no mesmo dia
        indexes = [models.Index(fields=["producao", "procedimento"])]

    def __str__(self):
        return f"{self.procedimento} x{self.quantidade} @ {self.valor_unitario}"

    @property
    def total(self):
        return (self.valor_unitario or Decimal("0")) * self.quantidade

    def clean(self):
        # validação conforme o tipo do procedimento
        if self.procedimento.tipo == Procedimento.TIPO_BOOLEANO and self.quantidade not in (0, 1):
            from django.core.exceptions import ValidationError
            raise ValidationError({"quantidade": "Para procedimentos booleanos, a quantidade deve ser 0 ou 1."})

    def save(self, *args, **kwargs):
        # se não foi definido explicitamente, pega o valor vigente na data da produção
        if self.valor_unitario in (None, Decimal("0")):
            data = self.producao.data
            pac = self.producao.paciente
            self.valor_unitario = ProcedimentoValor.valor_em(
                procedimento=self.procedimento,
                hospital=pac.hospital,
                convenio=pac.convenio,
                data=data
            )
        super().save(*args, **kwargs)
        # atualiza o agregado do dia
        self.producao.recomputar_total(save=True)