# Generated by Django 3.2 on 2021-05-01 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truequeapp', '0006_rename_truequesabierto_truequesabiertos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='truequesabiertos',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]