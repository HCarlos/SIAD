import os.path

import django.utils.timezone
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.urls import reverse

## -------------------------------------------------------------------------------
## MODEL EMPRESA
## -------------------------------------------------------------------------------


class Empresa(models.Model):
    empresa = models.CharField(max_length=250,null=True)
    rfc = models.CharField(max_length=13,null=True)
    domicilio_fiscal = models.CharField(max_length=250,null=True)
    representante_legal = models.CharField(max_length=250,null=True)

    def __str__(self):
        """String for representing the Model object."""
        return '{0}, {1}, {2}, {3}, {4}'.format(self.id, self.empresa, self.rfc, self.domicilio_fiscal, self.representante_legal)



## -------------------------------------------------------------------------------
## MODEL USUARIO
## -------------------------------------------------------------------------------
class Usuario(AbstractUser):
# class Usuario(models.Model):

    GENERO = [
        (1, 'Masculino'),
        (0, 'Femenino'),
    ]

    ESTATUS = [
        (1, 'Activo'),
        (0, 'Inactivo'),
    ]
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=250, default="", blank=True, null=True)
    ap_paterno = models.CharField(max_length=250,  blank=True, null=True)
    ap_materno = models.CharField(max_length=250,  blank=True, null=True)
    curp = models.CharField(max_length=18,  blank=True, null=True)
    emails = models.CharField(max_length=250,  blank=True, null=True)
    celulares = models.CharField(max_length=250, default="", blank=True, null=True)
    telefonos = models.CharField(max_length=250,  blank=True, null=True)
    fecha_nacimiento = models.DateField(default=django.utils.timezone.now,  blank=True, null=True)
    genero = models.SmallIntegerField(choices=GENERO, default=1, blank=True, null=True)
    session = models.CharField(max_length=250,  blank=True, null=True)
    estatus = models.SmallIntegerField(choices=ESTATUS, default=1, blank=True, null=True)
    empresa = models.ForeignKey(Empresa,on_delete=models.SET_NULL, blank=True, null=True)
    avatar = models.ImageField(upload_to="profile/", blank=True, null=True)
    avatar_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)
    # uploadedFile = models.FileField("usuarios", upload_to=path_and_rename("profile", 'usuario'), max_length=500,
    #                                 help_text="Ver archivo")



    class Meta:
        db_table = 'auth_user'
        permissions = (("Puede Crear", "Puede Editar"),)
        ordering = ['pk']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('user-view', kwargs={'pk': self.pk} )


    def Foto(self):
        archivo = 'media/{0}'.format(self.avatar)
        existe = os.path.isfile(archivo)
        if existe:
            return '/' + str(archivo)
        else:
            return '/static/images/web/empty_user_male.png' if self.genero == 1 else '/static/images/web/empty_user_female.png'

    def Genero(self):
        return 'Masculino' if self.genero == 1 else 'Femenino'

    def __str__(self):
        """String for representing the Model object."""
        return '{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}'.format(self.id, self.ap_paterno, self.ap_materno, self.nombre, self.curp, self.email, self.fecha_nacimiento, self.genero, self.emails, self.telefonos, self.celulares, self.avatar, self.username)
        # return self

