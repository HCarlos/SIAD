from datetime import datetime
from datetime import timedelta
import django.utils.timezone
import self
from django.db import models
from django.forms import ModelChoiceField
from django.urls import reverse


## -------------------------------------------------------------------------------
## MODEL DEPENDENCIA
## -------------------------------------------------------------------------------
import proyecto.models
from home.models import Usuario
from siad import settings
from siad.functions import validate_file_extension, file_size
from siad.settings import MEDIA_URL

class Dependencia(models.Model):
    """Model representing an dependencia."""
    dependencia = models.CharField(max_length=250)
    abreviatura = models.CharField(max_length=25)
    titular = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='dep_titular')
    modi_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='dep_modi_por')
    modi_el = models.DateField('died', null=True, blank=True)

    class Meta:
        verbose_name = 'Dependencia'
        verbose_name_plural = 'Dependencias'
        ordering = ['dependencia']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('dependencia', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0} - {1}.'.format(self.dependencia, self.abreviatura)


## -------------------------------------------------------------------------------
## MODEL SUBDIRECCIONES
## -------------------------------------------------------------------------------
class Subdireccione(models.Model):
    subdireccion = models.CharField(max_length=250)
    abreviatura = models.CharField(max_length=25)
    titular = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True, related_name='titular_subdirector')
    cargo = models.CharField(max_length=250)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.SET_NULL, null=True, related_name='subdir_dependencia')
    modi_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True, related_name='subdir_modi_por')
    modi_el = models.DateField('died', null=True, blank=True)

    class Meta:
        verbose_name = 'Subdirección'
        verbose_name_plural = 'Subdirecciones'
        ordering = ['subdireccion']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('subdireccion', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0} ({1}) => {2}'.format(self.subdireccion, self.abreviatura, self.titular)


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
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de medida'
        ordering = ['unidad']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('unidad', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        # return '{0} - {1}, {2}'.format(self.unidad, self.abreviatura, self.id)
        return '{0}'.format(self.unidad)




## -------------------------------------------------------------------------------
## MODEL RESPUESTAS OFICIO
## -------------------------------------------------------------------------------
class Respuestas(models.Model):

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
    archivo = models.FileField(upload_to="oficios_respuestas/{0}/{1}/{2}/".format(Fecha.year, Fecha.month, Fecha.day), blank=True, null=True, validators=[validate_file_extension, file_size])
    archivo_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True, related_name='respuesta_creado_por')
    creado_el = models.DateField('died', null=True, blank=True)
    modi_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True, related_name='respuesta_modi_por')
    modi_el = models.DateField('died', null=True, blank=True)

    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
        permissions = (("Puede Crear", "Puede Editar"),)
        ordering = ['-pk']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('respuesta-oficio-view', kwargs={'pk': self.pk})

    def get_absolute_archivo_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.archivo) if self.archivo else "#"

    def __str__(self):
        return '{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}'.format(self.id, self.respuesta, self.fecha_respuesta, self.archivo, self.creado_por, self.creado_el, self.modi_por, self.modi_el)

    def get_id(self):
        return "{0}".format(self.id)

    def get_respuesta_edit(self):
        return "/respuesta_edit/{0}".format(self.id)

    def get_respuesta_remove(self):
        return "/respuesta_remove/{0}".format(self.id)

    def get_respuesta(self):
        Ofi = Oficio.objects.get(respuestas__id=self.id)
        # return '%s' % self.archivo if self.archivo else ""
        return "file_{0}_{1}".format(Ofi.id, self.id) if self.archivo else "#"








## -------------------------------------------------------------------------------
## MODEL OFICIOS CONSULTA
## -------------------------------------------------------------------------------


# class Consecutivo:
#     def consecutivo(self):
#         return Oficio.objects.latest('consecutivo').consecutivo + 1

class Oficio(models.Model):

    TIPO_DOCUMENTO = [
        (0, 'RECIBIDOS'),
        (1, 'FIRMADOS POR EL(LA) DIRECTOR(A)'),
    ]
    Fecha = datetime.now()

    # Consecut =

    def get_fecha_respuesta():
        Fecha = datetime.now()
        return Fecha + timedelta(days=3)

    anno = models.IntegerField(default=Fecha.year, blank=True, null=True)
    tipo_documento = models.SmallIntegerField(choices=TIPO_DOCUMENTO, default=1, blank=True, null=True)
    consecutivo = models.IntegerField(default=0, blank=True, null=True)
    oficio = models.CharField(max_length=250, default="", blank=True, null=True)
    fecha_documento = models.DateField(default=django.utils.timezone.now,  blank=True, null=True)

    dir_remitente = models.ForeignKey(Dependencia, on_delete=models.SET_NULL, null=True, related_name='oficio_dir_remitente_dep')

    remitente = models.CharField(max_length=250, default="", blank=True, null=True)
    recibe = models.ForeignKey(Subdireccione, on_delete=models.SET_NULL, null=True, related_name='oficio_recibe_dep')
    # recibe = models.CharField(max_length=250, default="", blank=True, null=True)
    asunto = models.CharField(max_length=500, default="", blank=True, null=True)
    instrucciones = models.CharField(max_length=500, default="", blank=True, null=True)
    fecha_captura = models.DateField(default=django.utils.timezone.now, blank=True, null=True)
    fecha_recibido = models.DateField(default=django.utils.timezone.now, blank=True, null=True)
    fecha_respuesta = models.DateField(default=get_fecha_respuesta(), blank=True, null=True)
    subdireccion = models.ManyToManyField(Subdireccione)
    respuestas = models.ManyToManyField(Respuestas)
    archivo = models.FileField(upload_to="oficios/{0}/{1}/{2}/".format(Fecha.year,Fecha.month,Fecha.day), blank=True, null=True, validators=[validate_file_extension, file_size])
    archivo_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True, related_name='ofi_creado_por')
    creado_el = models.DateField(default=django.utils.timezone.now, null=True, blank=True)
    modi_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True, related_name='ofi_modi_por')
    modi_el = models.DateField(default=django.utils.timezone.now, null=True, blank=True)

    class Meta:
        verbose_name = 'Oficio'
        verbose_name_plural = 'Oficios'
        ordering = ['pk']

    # def my_date(self):
    #     return datetime.date(year=today.year - 1, month=today.month, day=today.day)
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('oficio-view', kwargs={'pk': self.pk} )

    @property
    def get_absolute_archivo_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.archivo) if self.archivo else "#"

    def get_oficio(self):
        return '%s' % self.oficio if self.archivo else ""

    def get_consecutivo(self):
        return self.objects.latest('consecutivo').consecutivo + 1

    def get_tipo_documento(self):
        return self.tipo_documento

    def get_id(self):
        return self.id

    def get_consecutivo(self):
        return self.consecutivo

    def __str__(self):
        """String for representing the Model object."""

        return '{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}'.format(
            self.id, self.anno, self.tipo_documento, self.consecutivo, self.oficio, self.fecha_documento, self.dir_remitente, self.remitente, self.recibe, self.asunto, self.instrucciones, self.fecha_respuesta, self.archivo, self.archivo_datetime, self.creado_por, self.creado_el, self.modi_por, self.modi_el)
        # return self

    def get_oficio_edit(self):
        return '/oficio_edit/{0}/{1}'.format(self.id, self.tipo_documento)

    def get_oficio_remove(self):
        return '/oficio_remove/{0}/{1}'.format(self.id, self.tipo_documento)

    def get_respuesta_new(self):
        return '/oficio_respuestas_list/{0}/{1}'.format(self.id, self.get_tipo_documento())





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
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
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






