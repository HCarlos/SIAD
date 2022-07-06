# Generated by Django 4.0 on 2022-07-06 19:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import siad.functions


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0001_initial'),
        ('home', '0009_alter_usuario_options'),
        ('oficiosenviados', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oficioenviado',
            name='subdireccion',
        ),
        migrations.AlterField(
            model_name='oficioenviado',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='oficios/2022/7/6/', validators=[siad.functions.validate_file_extension, siad.functions.file_size]),
        ),
        migrations.RemoveField(
            model_name='oficioenviado',
            name='recibe',
        ),
        migrations.AddField(
            model_name='oficioenviado',
            name='recibe',
            field=models.ManyToManyField(to='proyecto.Dependencia'),
        ),
        migrations.CreateModel(
            name='OficioEnviadoRespuestas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respuesta', models.CharField(default='', max_length=2000)),
                ('fecha_respuesta', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('estatus', models.SmallIntegerField(choices=[(0, 'RECIBIDO'), (1, 'EN PROCESO'), (2, 'TURNADO A OTRA DEPENDENCIA'), (3, 'NO PROCEDE'), (4, 'RESUELTO FAVORABLE'), (5, 'RESUELTO NO FAVORABLE')], default=0)),
                ('archivo', models.FileField(blank=True, null=True, upload_to='oficiosenviados_respuestas/2022/7/6/', validators=[siad.functions.validate_file_extension, siad.functions.file_size])),
                ('archivo_datetime', models.DateTimeField(auto_now=True, null=True)),
                ('creado_el', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('modi_el', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ofi_env_resp_creado_por', to='home.usuario')),
                ('modi_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ofi_env_resp_modi_por', to='home.usuario')),
            ],
            options={
                'verbose_name': 'Oficio Enviado Respuesta',
                'verbose_name_plural': 'Oficios Enviados Respuestas',
                'ordering': ['-pk'],
                'permissions': (('Puede Crear', 'Puede Editar'),),
            },
        ),
        migrations.AlterField(
            model_name='oficioenviado',
            name='respuestas',
            field=models.ManyToManyField(to='oficiosenviados.OficioEnviadoRespuestas'),
        ),
    ]
