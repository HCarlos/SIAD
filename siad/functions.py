import os
from uuid import uuid4

import required as required
from django import forms
from django.contrib.auth.models import UserManager
from django.forms import ModelForm, EmailInput, PasswordInput, TextInput, FileInput, Select

from home.models import Usuario

# ************************************************
# MODEL FORM DE USUARIO (BASICO)
# ************************************************

class UserFormBasic(ModelForm):
    # username = forms.CharField(required=True)
    # email = forms.CharField(required=True)
    # password = forms.CharField(required=True)

    class Meta:
        model = Usuario
        fields = ['username', 'password', 'email', 'ap_paterno', 'ap_materno', 'nombre', 'curp']
        widgets = {
            'username': TextInput(attrs={'type': 'text', 'required': 'false', 'placeholder': 'Escribe el Username'}),
            'email': EmailInput(attrs={'type': 'email', 'class': 'form-control', 'placeholder': 'Escribe el Email'}),
            'password': PasswordInput(attrs={'type': 'password', 'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(UserFormBasic, self).__init__(*args, **kwargs)
        self.fields['ap_paterno'].required = False
        self.fields['ap_materno'].required = False
        self.fields['curp'].required = False
        self.fields['nombre'].required = False


# ************************************************
# MODEL FORM PARA FOTO
# ************************************************

class UserFormFoto(ModelForm):

    class Meta:
        model = Usuario
        # fields = '__all__'
        fields = ['id', 'avatar']
        # widgets = {
        #     'id': TextInput(attrs={'type': 'text'}),
        #     'avatar': FileInput(attrs={'type': 'file', 'required': 'true', 'placeholder': 'Selecciona una imagen'}),
        # }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserFormFoto, self).__init__(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     kwargs['commit'] = False
    #     obj = super(UserFormFoto, self).save(*args, **kwargs)
    #     if self.request:
    #         obj.user = self.request.user
    #     obj.save()
    #     return obj
