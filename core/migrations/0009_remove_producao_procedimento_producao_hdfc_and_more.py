# Generated by Django 4.2.4 on 2023-09-04 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_producao_cateter_producao_valor_cateter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producao',
            name='procedimento',
        ),
        migrations.AddField(
            model_name='producao',
            name='hdfc',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='producao',
            name='hemodialise',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='producao',
            name='parecer_visita',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='producao',
            name='valor_hdfc',
            field=models.FloatField(default=400),
        ),
        migrations.AddField(
            model_name='producao',
            name='valor_hemodialise',
            field=models.FloatField(default=120),
        ),
        migrations.AddField(
            model_name='producao',
            name='valor_parecer',
            field=models.FloatField(default=75),
        ),
        migrations.AlterField(
            model_name='producao',
            name='valor_cateter',
            field=models.IntegerField(default=150),
        ),
    ]
