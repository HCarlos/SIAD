# Generated by Django 4.0 on 2021-12-29 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0002_remove_oficio_sad_remove_oficio_sai_remove_oficio_se_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='eventos/2021/12/29/'),
        ),
        migrations.AlterField(
            model_name='oficio',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='oficios/2021/12/29/'),
        ),
        migrations.AlterField(
            model_name='oficioconsulta',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='oficios_consulta/2021/12/29/'),
        ),
    ]