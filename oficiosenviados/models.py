from datetime import datetime, timedelta

import django
from django.db import models

# Create your models here.

## -------------------------------------------------------------------------------
## MODEL OFICIOS CONSULTA
## -------------------------------------------------------------------------------

from django.urls import reverse

from home.models import Usuario
from proyecto.models import Subdireccione, Dependencia, Respuestas, UnidadAdministrativa
from siad import settings
from siad.functions import validate_file_extension, file_size



## -------------------------------------------------------------------------------
## MODEL RESPUESTAS OFICIO
## -------------------------------------------------------------------------------
class OficioEnviadoRespuestas(models.Model):

    ESTATUS = [
        (0, 'RECIBIDO'),
        (1, 'EN PROCESO'),
        (2, 'TURNADO A OTRA DEPENDENCIA'),
        (3, 'NO PROCEDE'),
        (4, 'RESUELTO FAVORABLE'),
        (5, 'RESUELTO NO FAVORABLE'),
    ]

    Fecha = datetime.now()
    respuesta = models.CharField(max_length=2000, default="", blank=False, null=False)
    fecha_respuesta = models.DateField(default=django.utils.timezone.now, blank=True, null=True)
    estatus = models.SmallIntegerField(choices=ESTATUS, default=0, blank=False, null=False)
    archivo = models.FileField(upload_to="oficiosenviados_respuestas/{0}/{1}/{2}/".format(Fecha.year, Fecha.month, Fecha.day), blank=True, null=True, validators=[validate_file_extension, file_size])
    archivo_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True, related_name='ofi_env_resp_creado_por')
    creado_el = models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)
    modi_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True, related_name='ofi_env_resp_modi_por')
    modi_el = models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)

    class Meta:
        verbose_name = 'Oficio Enviado Respuesta'
        verbose_name_plural = 'Oficios Enviados Respuestas'
        permissions = (("Puede Crear", "Puede Editar"),)
        ordering = ['-pk']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('oficio-enviado-respuesta-oficio-view', kwargs={'pk': self.pk})

    def get_absolute_archivo_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.archivo) if self.archivo else "#"

    def __str__(self):
        return '{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}'.format(self.id, self.respuesta, self.fecha_respuesta, self.archivo, self.creado_por, self.creado_el, self.modi_por, self.modi_el)

    def get_id(self):
        return "{0}".format(self.id)

    def get_respuesta_edit(self):
        return "/oficioenviado_respuesta_edit/{0}".format(self.id)

    def get_respuesta_remove(self):
        return "/oficioenviado_respuesta_remove/{0}".format(self.id)

    def get_respuesta(self):
        Ofi = OficioEnviado.objects.get(respuestas__id=self.id)
        # return '%s' % self.archivo if self.archivo else ""
        return "file_{0}_{1}".format(Ofi.id, self.id) if self.archivo else "#"







class OficioEnviado(models.Model):


    Fecha = datetime.now()

    anno = models.IntegerField(default=Fecha.year, blank=True, null=True)
    consecutivo = models.IntegerField(default=0, blank=True, null=True)
    oficio = models.CharField(max_length=250, default="", blank=True, null=True)
    remitente =  models.ForeignKey(Subdireccione, on_delete=models.SET_NULL, null=True, related_name='oficio_enviado_remitente_dep')
    asunto = models.CharField(max_length=500, default="", blank=True, null=True)
    instrucciones = models.CharField(max_length=500, default="", blank=True, null=True)
    fecha_documento = models.DateField(default=django.utils.timezone.now,  blank=True, null=True)
    fecha_captura = models.DateField(default=django.utils.timezone.now, blank=True, null=True)
    fecha_recibido = models.DateField(default=django.utils.timezone.now, blank=True, null=True)
    dependencias = models.ManyToManyField(Dependencia)
    respuestas = models.ManyToManyField(OficioEnviadoRespuestas)
    archivo = models.FileField(upload_to="oficios/{0}/{1}/{2}/".format(Fecha.year, Fecha.month, Fecha.day), blank=True, null=True, validators=[validate_file_extension, file_size])
    archivo_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)
    unidad_administrativa = models.ForeignKey(UnidadAdministrativa, on_delete=models.SET_NULL, null=True, related_name='ua_ofi_env_unidad_administrativa')
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True, related_name='ofi_env_creado_por')
    creado_el = models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)
    modi_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True, related_name='ofi_env_modi_por')
    modi_el = models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)

    class Meta:
        verbose_name = 'Oficio Enviado'
        verbose_name_plural = 'Oficios Enviados'
        ordering = ['pk']


    def __str__(self):
        return '{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}'.format(
            self.id, self.anno, self.consecutivo, self.oficio, self.fecha_documento, self.remitente, self.remitente, self.del_remitente, self.recibe, self.asunto, self.instrucciones, self.archivo, self.archivo_datetime, self.creado_por, self.creado_el, self.modi_por, self.modi_el, self.unidad_administrativa)

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('oficioenviado-view', kwargs={'pk': self.pk} )

    @property
    def get_absolute_archivo_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.archivo) if self.archivo else "#"

    def get_oficio(self):
        return '%s' % self.oficio if self.archivo else ""

    def get_consecutivo(self):
        return self.objects.latest('consecutivo').consecutivo + 1

    def get_id(self):
        return self.id

    def get_consecutivo(self):
        return self.consecutivo

    def get_respuestas_count(self):
        return self.objects.filter(respuestas__oficioenviado__oficio=self.id).count

    @property
    def get_del_remitente(self):
        # Remitente = self.remitente
        nombre_completo = self.remitente.titular.get_nombre_completo
        username = self.remitente.titular.username
        return "{0} ({1})".format(nombre_completo, username)

    def get_oficio_edit(self):
        return '/oficioenviado_edit/{0}'.format(self.id)

    def get_consec(self):
        consec = self.objects.all().reverse()[0]
        if consec > 0:
            return consec + 1
        else:
            return 1

    def get_oficio_remove(self):
        return '/oficioenviado_remove/{0}'.format(self.id)

    def get_respuesta_new(self):
        return '/oficioenviado_respuestas_list/{0}'.format(self.id)

