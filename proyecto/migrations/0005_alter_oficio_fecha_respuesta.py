# Generated by Django 4.0 on 2022-07-06 23:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0004_alter_oficio_fecha_respuesta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oficio',
            name='fecha_respuesta',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 7, 9, 18, 1, 47, 251674), null=True),
        ),
    ]