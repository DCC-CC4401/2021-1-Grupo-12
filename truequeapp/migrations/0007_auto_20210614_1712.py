# Generated by Django 2.2.5 on 2021-06-14 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truequeapp', '0006_alter_usuario_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
    ]
