import datetime
from bootstrap_datepicker_plus.widgets import DatePickerInput, DateTimePickerInput
from django.forms import ModelForm, TextInput, ModelChoiceField, Textarea, Select
from django import forms
from django.utils import timezone

from home.models import Usuario
from proyecto.models import Oficio, Dependencia, Subdireccione, Respuestas
from siad import settings
from django.forms.fields import DateField, DateTimeField


## -------------------------------------------------------------------------------
## MODEL FORM OFICIOS
## -------------------------------------------------------------------------------

class OficioForm(ModelForm):
    dir_remitente = ModelChoiceField(label='Dependencia', queryset=Dependencia.objects.all())
    recibe = ModelChoiceField(label='Recibe', queryset=Subdireccione.objects.all())

    fecha_documento = DateField(widget=DatePickerInput(format=settings.DATE_FORMAT))
    fecha_captura = DateField(widget=DatePickerInput(format=settings.DATE_FORMAT))
    fecha_respuesta = DateField(widget=DatePickerInput(format=settings.DATE_FORMAT))
    fecha_recibido = DateField(widget=DatePickerInput(format=settings.DATE_FORMAT))

    # creado_por = ModelChoiceField(label='Creado Por', empty_label=None, queryset=Usuario.objects.filter(id=1))
    # modi_por = ModelChoiceField(label='Modificado Por', empty_label=None, queryset=Usuario.objects.filter(id=1))

    instrucciones = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'cols': 5}))

    class DateInput(forms.DateInput):
        input_type = 'date'

    class Meta:
        model = Oficio
        fields = '__all__'
        exclude = ['respuestas', 'archivo_datetime']
        widgets = {
                      'remitente': TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
                      'del_remitente': TextInput(attrs={'class': 'form-control'}),
                      'recibe': TextInput(attrs={'class': 'form-control'}),
                      'instrucciones': Textarea(attrs={'class': 'form-control', 'rows': 45, 'cols': 80}),
                      'asunto': Textarea(attrs={'class': 'form-control', 'rows': 45, 'cols': 80}),
                      'creado_por': Select(attrs={'readonly': 'readonly', 'class': 'form-control'}),
                      'modi_por': Select(attrs={'readonly': 'readonly', 'class': 'form-control'}),
                  },

        labels = {
            "anno": "Año",
            "tipo_documento": "Tipo de Oficio",
            "dir_remitente": "dir_remitente(*)",
            "del_remitente": "Escriba el Remitente:",
            "recibe": "Recibe ó Emite:",
        }

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        oficio_id = kwargs.pop('oficio_id', None)
        super(OficioForm, self).__init__(*args, **kwargs)
        self.fields['dir_remitente'].queryset = Dependencia.objects.all()
        self.fields['recibe'].queryset = Subdireccione.objects.all()
        self.fields['tipo_documento'].widget = forms.HiddenInput()
        self.fields['creado_por'].empty_label = None
        self.fields['modi_por'].empty_label = None
        self.initial['modi_por'] = user_id
        self.initial['modi_el'] = datetime.datetime.now()

        self.fields['creado_por'].queryset = Usuario.objects.filter(pk=user_id)
        self.fields['modi_por'].queryset = Usuario.objects.filter(pk=user_id)

        # if oficio_id <= 0:
        #     self.fields['creado_por'].queryset = Usuario.objects.filter(pk=user_id)
        #     self.fields['modi_por'].queryset = Usuario.objects.filter(pk=user_id)
        # else:
        #     self.fields['creado_por'].widget = forms.HiddenInput()
        #     self.fields['modi_por'].widget = forms.HiddenInput()


        # if oficio_id > 0:
        #     self.fields['creado_por'].widget = forms.HiddenInput()
        #     self.fields['modi_por'].widget = forms.HiddenInput()

        self.fields['modi_el'].widget = forms.HiddenInput()
        self.fields['creado_el'].widget = forms.HiddenInput()

        self.fields['remitente'].widget.attrs['readonly'] = True

    def set_consecutivo(self, consec):
        self.fields['consecutivo'].widget.attrs['readonly'] = False
        self.initial['consecutivo'] = consec
        self.fields['consecutivo'].widget.attrs['readonly'] = False

    def get_consecutivo(self, TD):
        return Oficio.objects.filter(tipo_documento=TD).latest('consecutivo').consecutivo + 1

    def set_tipo_documento(self, td):
        self.initial['tipo_documento'] = td

    def get_tipo_documento(self):
        return self.tipo_documento

    def set_remitente(self, remitente):
        self.fields['remitente'].widget.attrs['readonly'] = False
        self.initial['remitente'] = remitente
        self.fields['remitente'].widget.attrs['readonly'] = True

    def get_remitente(self):
        return self.remitente

    def set_modi_por(self, modi_por):
        self.initial['modi_por'] = modi_por

    def set_modi_el(self, modi_el):
        self.initial['modi_por'] = modi_el


## -------------------------------------------------------------------------------
## MODEL FORM RESPUESTAS
## -------------------------------------------------------------------------------

class RespuestaForm(ModelForm):
    fecha_respuesta = DateField(
        widget=forms.widgets.DateInput(format='%d/%m/%Y', attrs={'type': 'date', 'class': ' text-bold'}),
        input_formats=settings.DATE_INPUT_FORMATS,
        label="Fecha de esta respuesta"
    )

    respuesta = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'cols': 5}),
        label="Mi Respuesta"
    )

    class Meta:
        model = Respuestas
        fields = '__all__'
        exclude = ['archivo_datetime', 'creado_por', 'creado_el', 'modi_por', 'modi_el']
        widgets = {
                      'respuesta': Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 5}),
                  },
        labels = {
            "fecha_respuesta": "Fecha de Respuesta",
            "respuesta": "Respuesta",
        }

    def __init__(self, *args, **kwargs):
        super(RespuestaForm, self).__init__(*args, **kwargs)
        self.initial['fecha_respuesta'] = self.instance.fecha_respuesta.isoformat()
        print("HA INICIADO BIEN")

    def get_id(self):
        return "{0}".format(self.id)
