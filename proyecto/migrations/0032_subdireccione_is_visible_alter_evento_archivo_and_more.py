# Generated by Django 4.0 on 2022-05-12 17:07

import datetime
from django.db import migrations, models
import siad.functions


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0031_alter_oficio_fecha_respuesta_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subdireccione',
            name='is_visible',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='evento',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='eventos/2022/5/12/'),
        ),
        migrations.AlterField(
            model_name='oficio',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='oficios/2022/5/12/', validators=[siad.functions.validate_file_extension, siad.functions.file_size]),
        ),
        migrations.AlterField(
            model_name='oficio',
            name='fecha_respuesta',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 5, 15, 12, 7, 45, 334632), null=True),
        ),
        migrations.AlterField(
            model_name='respuestas',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='oficios_respuestas/2022/5/12/', validators=[siad.functions.validate_file_extension, siad.functions.file_size]),
        ),
    ]