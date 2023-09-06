# Generated by Django 4.2.4 on 2023-09-04 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_condutadescricao_alter_conduta_descricao'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcessoDescricao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Acesso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_implantacao', models.DateField()),
                ('dias_acesso', models.IntegerField(blank=True, null=True)),
                ('criado_em', models.DateField(auto_now_add=True)),
                ('criado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('nome', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.acessodescricao')),
                ('paciente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.paciente')),
            ],
        ),
    ]