# Generated by Django 2.2.20 on 2021-06-08 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truequeapp', '0002_auto_20210504_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicacion',
            name='completado',
            field=models.CharField(choices=[('A', 'Activo'), ('E', 'Eliminado'), ('I', 'Inactivo')], default='A', max_length=1),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
    ]