# Generated by Django 3.2 on 2021-06-17 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('truequeapp', '0006_alter_usuario_first_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_de_envio', models.DateTimeField(auto_now_add=True)),
                ('tipo', models.CharField(choices=[('C', 'Calificar'), ('R', 'Revisar'), ('A', 'Aceptar')], max_length=1)),
                ('estado', models.CharField(choices=[('V', 'Visto'), ('N', 'No visto')], max_length=1)),
                ('trueque_asoc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='truequeapp.trueque')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
