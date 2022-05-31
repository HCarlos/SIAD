# Generated by Django 4.0 on 2022-05-31 18:10

import datetime
from django.db import migrations, models
import siad.functions


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0037_alter_oficio_fecha_respuesta'),
    ]

    operations = [
        migrations.AddField(
            model_name='oficio',
            name='del_remitente',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='evento',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='eventos/2022/5/31/'),
        ),
        migrations.AlterField(
            model_name='oficio',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='oficios/2022/5/31/', validators=[siad.functions.validate_file_extension, siad.functions.file_size]),
        ),
        migrations.AlterField(
            model_name='oficio',
            name='fecha_respuesta',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 6, 3, 13, 10, 15, 814408), null=True),
        ),
        migrations.AlterField(
            model_name='respuestas',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='oficios_respuestas/2022/5/31/', validators=[siad.functions.validate_file_extension, siad.functions.file_size]),
        ),
    ]