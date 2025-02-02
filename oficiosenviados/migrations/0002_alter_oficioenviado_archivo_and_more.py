# Generated by Django 4.0 on 2022-10-05 20:35

from django.db import migrations, models
import siad.functions


class Migration(migrations.Migration):

    dependencies = [
        ('oficiosenviados', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oficioenviado',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='oficios/2022/10/5/', validators=[siad.functions.validate_file_extension, siad.functions.file_size]),
        ),
        migrations.AlterField(
            model_name='oficioenviadorespuestas',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='oficiosenviados_respuestas/2022/10/5/', validators=[siad.functions.validate_file_extension, siad.functions.file_size]),
        ),
    ]
