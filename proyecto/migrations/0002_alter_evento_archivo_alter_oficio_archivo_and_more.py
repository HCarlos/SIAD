# Generated by Django 4.0 on 2022-07-01 20:34

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import siad.functions


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_usuario_options'),
        ('proyecto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='eventos/2022/7/1/'),
        ),
        migrations.AlterField(
            model_name='oficio',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='oficios/2022/7/1/', validators=[siad.functions.validate_file_extension, siad.functions.file_size]),
        ),
        migrations.AlterField(
            model_name='oficio',
            name='creado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ofi_creado_por', to='home.usuario'),
        ),
        migrations.AlterField(
            model_name='oficio',
            name='fecha_respuesta',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 7, 4, 15, 34, 17, 959416), null=True),
        ),
        migrations.AlterField(
            model_name='oficio',
            name='modi_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ofi_modi_por', to='home.usuario'),
        ),
        migrations.AlterField(
            model_name='respuestas',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='oficios_respuestas/2022/7/1/', validators=[siad.functions.validate_file_extension, siad.functions.file_size]),
        ),
        migrations.CreateModel(
            name='UnidadAdministrativa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidad', models.CharField(max_length=250)),
                ('abreviatura', models.CharField(max_length=25)),
                ('modi_el', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('modi_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ua_modi_por', to='home.usuario')),
                ('titular', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ua_titular', to='home.usuario')),
            ],
            options={
                'verbose_name': 'UnidadAdministrativa',
                'verbose_name_plural': 'UnidadesAdministrativas',
                'ordering': ['unidad'],
            },
        ),
    ]