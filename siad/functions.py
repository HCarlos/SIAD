import os
from django.forms import ModelForm, EmailInput, PasswordInput, TextInput, FileInput, Select
from home.models import Usuario
from django.core.exceptions import ValidationError


# ************************************************
# MODEL FORM DE USUARIO (BASICO)
# ************************************************

class UserFormBasic(ModelForm):

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
        fields = ['id', 'avatar']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserFormFoto, self).__init__(*args, **kwargs)

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.xlsx', '.xls', '.doc', '.docx', '.ppt', '.pptx']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Ay problemas!!! no soporto ese tipo de archivo!!!')

def file_size(value):
    limit = 100 * (1024 * 1024)
    valor = limit / (1024 * 1024)
    if value.size > limit:
        raise ValidationError('Archivo demasiado pesado. Solo puedes subir archivos de %s gb' % valor)
