# Generated by Django 4.2.4 on 2023-09-05 03:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_hospital_valor_cateter_hospital_valor_hdfc_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producao',
            name='valor_cateter',
        ),
        migrations.RemoveField(
            model_name='producao',
            name='valor_hdfc',
        ),
        migrations.RemoveField(
            model_name='producao',
            name='valor_hemodialise',
        ),
        migrations.RemoveField(
            model_name='producao',
            name='valor_parecer',
        ),
    ]
