# Generated by Django 4.2.4 on 2023-09-04 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_producao_cateter_remove_producao_hdfc_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='producao',
            name='cateter',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='producao',
            name='valor_cateter',
            field=models.IntegerField(default=75),
        ),
    ]