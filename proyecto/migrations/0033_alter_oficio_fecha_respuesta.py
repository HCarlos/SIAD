# Generated by Django 4.0 on 2022-05-12 22:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0032_subdireccione_is_visible_alter_evento_archivo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oficio',
            name='fecha_respuesta',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 5, 15, 17, 3, 53, 492300), null=True),
        ),
    ]