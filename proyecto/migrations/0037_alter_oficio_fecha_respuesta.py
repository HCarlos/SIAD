# Generated by Django 4.0 on 2022-05-12 22:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0036_alter_oficio_fecha_respuesta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oficio',
            name='fecha_respuesta',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 5, 15, 17, 12, 29, 457910), null=True),
        ),
    ]