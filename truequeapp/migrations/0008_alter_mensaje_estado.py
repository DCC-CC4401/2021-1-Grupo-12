# Generated by Django 3.2 on 2021-06-17 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truequeapp', '0007_mensaje'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensaje',
            name='estado',
            field=models.CharField(choices=[('V', 'Visto'), ('N', 'No visto')], default='N', max_length=1),
        ),
    ]
