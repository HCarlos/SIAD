from datetime import datetime
import django.utils.timezone
from django.db import models
from django.forms import ModelChoiceField
from django.urls import reverse
from home.models import Usuario

## -------------------------------------------------------------------------------
## MODEL DEPENDENCIA
## -------------------------------------------------------------------------------
class Dependencia(models.Model):
    """Model representing an dependencia."""
    dependencia = models.CharField(max_length=250)
    abreviatura = models.CharField(max_length=25)
    titular = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='dep_titular')
    modi_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True, related_name='dep_modi_por')
    modi_el = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['dependencia']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('dependencia', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}, {1}'.format(self.id, self.dependencia)


## -------------------------------------------------------------------------------
## MODEL SUBDIRECCIONES
## -------------------------------------------------------------------------------
class Subdireccione(models.Model):
    subdireccion = models.CharField(max_length=250)
    titutlar = models.CharField(max_length=250)
    cargo = models.CharField(max_length=250)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.SET_NULL, null=True, related_name='subdir_dependencia')
    modi_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True, related_name='subdir_modi_por')
    modi_el = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['subdireccion']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('subdireccion', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}, {1}, {2}, {3}, {4}'.format(self.id, self.subdireccion, self.titutlar, self.cargo, self.dependencia)


## -------------------------------------------------------------------------------
## MODEL UNIDAD DE MEDIDAS
## -------------------------------------------------------------------------------
class UnidadMedida(models.Model):
    """Model representing an dependencia."""
    unidad = models.CharField(max_length=250)
    abreviatura = models.CharField(max_length=25)
    modi_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True, related_name='medida_modi_por')
    modi_el = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['unidad']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('unidad', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}, {1}, {2}'.format(self.id, self.unidad, self.abreviatura)


## -------------------------------------------------------------------------------
## MODEL OFICIOS CONSULTA
## -------------------------------------------------------------------------------
#
# class OficioConsulta(models.Model):
#     Fecha = datetime.now()
#     oficio = models.CharField(max_length=250, default="", blank=True, null=True)
#     fecha_oficio = models.DateField(default=django.utils.timezone.now,  blank=True, null=True)
#     asunto = models.CharField(max_length=500, default="", blank=True, null=True)
#     fecha_respuesta = models.DateField(default=django.utils.timezone.now, blank=True, null=True)
#     uea = models.BooleanField(default=False,  blank=True, null=True)
#     seif = models.BooleanField(default=False,  blank=True, null=True)
#     se = models.BooleanField(default=False,  blank=True, null=True)
#     sad = models.BooleanField(default=False,  blank=True, null=True)
#     snpi = models.BooleanField(default=False,  blank=True, null=True)
#     sfo = models.BooleanField(default=False,  blank=True, null=True)
#     st = models.BooleanField(default=False,  blank=True, null=True)
#     sai = models.BooleanField(default=False,  blank=True, null=True)
#     archivo = models.FileField(upload_to="oficios_consulta/{0}/{1}/{2}/".format(Fecha.year,Fecha.month,Fecha.day), blank=True, null=True)
#     archivo_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)
#     creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='oficon_creado_por')
#     creado_el = models.DateField('died', null=True, blank=True)
#     modi_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='oficon_modi_por')
#     modi_el = models.DateField('died', null=True, blank=True)
#
#     class Meta:
#             permissions = (("Puede Crear", "Puede Editar"),)
#             ordering = ['pk']
#
#     def get_absolute_url(self):
#         """Returns the url to access a particular author instance."""
#         return reverse('oficio-view', kwargs={'pk': self.pk} )
#
#     def __str__(self):
#         """String for representing the Model object."""
#         return '{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}'.format(self.id, self.oficio, self.fecha_oficio, self.asunto, self.fecha_respuesta, self.uea, self.seif, self.se, self.sad, self.snpi, self.sfo, self.st, self.sai, self.archivo, self.archivo_datetime, self.creado_por, self.creado_el, self.modi_por, self.modi_el)
#         # return self



## -------------------------------------------------------------------------------
## MODEL OFICIOS CONSULTA
## -------------------------------------------------------------------------------
class Oficio(models.Model):

    TIPO_DOCUMENTO = [
        (0, 'RECIBIDO'),
        (1, 'FIRMADO POR EL(LA) DIRECTOR(A)'),
    ]

    Fecha = datetime.now()
    anno = models.IntegerField(default=Fecha.year, blank=True, null=True)
    tipo_documento = models.SmallIntegerField(choices=TIPO_DOCUMENTO, default=1, blank=True, null=True)
    consecutivo = models.IntegerField(default=0, blank=True, null=True)
    oficio = models.CharField(max_length=250, default="", blank=True, null=True)
    fecha_documento = models.DateField(default=django.utils.timezone.now,  blank=True, null=True)

    dir_remitente = models.ForeignKey(Dependencia, on_delete=models.SET_NULL, null=True, related_name='oficio_dir_remitente_dep')

    # remitente = models.ForeignKey(Dependencia.titular, on_delete=models.SET_NULL, null=True, related_name='titular_dir_remitente_dep')
    # recibe = models.ForeignKey(Dependencia.titular, on_delete=models.SET_NULL, null=True, related_name='recibe_oficio_dep')

    remitente = models.CharField(max_length=250, default="", blank=True, null=True)
    recibe = models.CharField(max_length=250, default="", blank=True, null=True)
    asunto = models.CharField(max_length=500, default="", blank=True, null=True)
    instrucciones = models.CharField(max_length=500, default="", blank=True, null=True)
    fecha_captura = models.DateField(default=django.utils.timezone.now, blank=True, null=True)
    fecha_respuesta = models.DateField(default=django.utils.timezone.now, blank=True, null=True)
    archivo = models.FileField(upload_to="oficios/{0}/{1}/{2}/".format(Fecha.year,Fecha.month,Fecha.day), blank=True, null=True)
    archivo_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True, related_name='ofi_creado_por')
    creado_el = models.DateField('died', null=True, blank=True)
    modi_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True, related_name='ofi_modi_por')
    modi_el = models.DateField('died', null=True, blank=True)

    class Meta:
            permissions = (("Puede Crear", "Puede Editar"),)
            ordering = ['pk']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('oficio-view', kwargs={'pk': self.pk} )

    def __str__(self):
        """String for representing the Model object."""

        return '{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}'.format(
            self.id, self.anno, self.tipo_documento, self.consecutivo, self.oficio, self.fecha_oficio, self.dir_remitente, self.remitente, self.recibe, self.asunto, self.instrucciones, self.fecha_respuesta, self.archivo, self.archivo_datetime, self.creado_por, self.creado_el, self.modi_por, self.modi_el)
        # return self

    def get_oficio_edit(self):
        return '/oficio_edit/{0}'.format(self.id)

    def get_oficio_remove(self):
        return '/oficio_remove/{0}'.format(self.id)


## -------------------------------------------------------------------------------
## MODEL OFICIOS CONSULTA
## -------------------------------------------------------------------------------
class Evento(models.Model):
    Fecha = datetime.now()
    anno = models.IntegerField(default=Fecha.year, blank=True, null=True)
    fecha_evento = models.DateField(default=django.utils.timezone.now,  blank=True, null=True)
    hora_evento = models.TimeField(default=django.utils.timezone.now,  blank=True, null=True)
    asunto = models.CharField(max_length=500, default="", blank=True, null=True)
    lugar = models.CharField(max_length=500, default="", blank=True, null=True)
    dependencia_solicita = models.ForeignKey(Dependencia, on_delete=models.SET_NULL, null=True, related_name='evento_solicita_dep')
    seguimiento = models.TextField(max_length=4000, default="", blank=True, null=True)
    respuesta = models.TextField(max_length=4000, default="", blank=True, null=True)
    fecha_respuesta = models.DateField(default=django.utils.timezone.now, blank=True, null=True)
    archivo = models.FileField(upload_to="eventos/{0}/{1}/{2}/".format(Fecha.year,Fecha.month,Fecha.day), blank=True, null=True)
    archivo_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True, related_name='evento_creado_por')
    creado_el = models.DateField('died', null=True, blank=True)
    modi_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True, related_name='evento_modi_por')
    modi_el = models.DateField('died', null=True, blank=True)

    class Meta:
            permissions = (("Puede Crear", "Puede Editar"),)
            ordering = ['pk']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('oficio-view', kwargs={'pk': self.pk} )

    def __str__(self):
        """String for representing the Model object."""
        return '{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}'.format(
            self.id, self.anno, self.fecha_evento, self.hora_evento, self.asunto, self.lugar, self.dependencia_solicita, self.seguimiento, self.respuesta, self.fecha_respuesta, self.archivo, self.archivo_datetime, self.creado_por, self.creado_el, self.modi_por, self.modi_el)
        # return self






