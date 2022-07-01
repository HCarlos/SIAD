# Generated by Django 4.0 on 2022-07-01 20:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0002_alter_evento_archivo_alter_oficio_archivo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dependencia',
            name='unidad_administrativa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ua_dep_unidad_administrativa', to='proyecto.unidadadministrativa'),
        ),
        migrations.AddField(
            model_name='evento',
            name='unidad_administrativa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ua_evento_unidad_administrativa', to='proyecto.unidadadministrativa'),
        ),
        migrations.AddField(
            model_name='oficio',
            name='unidad_administrativa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ua_ofi_unidad_administrativa', to='proyecto.unidadadministrativa'),
        ),
        migrations.AddField(
            model_name='subdireccione',
            name='unidad_administrativa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ua_subdir_unidad_administrativa', to='proyecto.unidadadministrativa'),
        ),
        migrations.AlterField(
            model_name='oficio',
            name='fecha_respuesta',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 7, 4, 15, 45, 18, 317177), null=True),
        ),
    ]
