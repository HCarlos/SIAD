# Generated by Django 4.0 on 2022-02-24 01:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0018_rename_titutlar_subdireccione_titular_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oficio',
            name='fecha_respuesta',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 2, 25, 19, 26, 18, 716921), null=True),
        ),
        migrations.AlterField(
            model_name='oficio',
            name='tipo_documento',
            field=models.SmallIntegerField(blank=True, choices=[(0, 'RECIBIDOS'), (1, 'FIRMADOS POR EL(LA) DIRECTOR(A)')], default=1, null=True),
        ),
    ]
