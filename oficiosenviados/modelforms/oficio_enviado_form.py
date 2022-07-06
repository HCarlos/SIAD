## -------------------------------------------------------------------------------
## MODEL FORM OFICIOS
## -------------------------------------------------------------------------------
import datetime

from bootstrap_datepicker_plus.widgets import DatePickerInput, DateTimePickerInput
from django import forms
from django.forms import ModelForm, ModelChoiceField, DateField, TextInput, Textarea, Select, DateTimeField

from home.models import Usuario
from oficiosenviados.models import OficioEnviado, OficioEnviadoRespuestas
from proyecto.models import Dependencia, UnidadAdministrativa, Subdireccione
from siad import settings


class OficioEnviadoForm(ModelForm):
    remitente = ModelChoiceField(label='Remitente', queryset=Subdireccione.objects.all())
    unidad_administrativa = ModelChoiceField(label='Unidad Administrativa', queryset=UnidadAdministrativa.objects.all())
    # recibe = ModelChoiceField(label='Recibe', queryset=Dependencia.objects.all())

    fecha_documento = DateField(widget=DatePickerInput(format=settings.DATE_FORMAT))
    fecha_captura = DateField(widget=DatePickerInput(format=settings.DATE_FORMAT))
    # fecha_respuesta = DateField(widget=DatePickerInput(format=settings.DATE_FORMAT))
    fecha_recibido = DateField(widget=DatePickerInput(format=settings.DATE_FORMAT))

    # creado_por = ModelChoiceField(label='Creado Por', empty_label=None, queryset=Usuario.objects.filter(id=1))
    # modi_por = ModelChoiceField(label='Modificado Por', empty_label=None, queryset=Usuario.objects.filter(id=1))

    instrucciones = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'cols': 5}))

    class DateInput(forms.DateInput):
        input_type = 'date'

    class Meta:
        model = OficioEnviado
        fields = '__all__'
        exclude = ['respuestas', 'archivo_datetime']
        widgets = {
                      'remitente': TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
                      'instrucciones': Textarea(attrs={'class': 'form-control', 'rows': 45, 'cols': 80}),
                      'asunto': Textarea(attrs={'class': 'form-control', 'rows': 45, 'cols': 80}),
                      'creado_por': Select(attrs={'readonly': 'readonly', 'class': 'form-control'}),
                      'modi_por': Select(attrs={'readonly': 'readonly', 'class': 'form-control'}),
                  },

        labels = {
            "anno": "Año",
            "remitente": "remitente",
            "del_remitente": "Escriba el Remitente:",
            "recibe": "Recibe ó Emite:",
        }

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        oficio_id = kwargs.pop('oficioenviado_id', None)
        super(OficioEnviadoForm, self).__init__(*args, **kwargs)
        self.fields['remitente'].queryset = Subdireccione.objects.all()
        self.fields['unidad_administrativa'].queryset = UnidadAdministrativa.objects.all()
        self.fields['unidad_administrativa'].empty_label = None
        # self.fields['recibe'].queryset = Subdireccione.objects.all()
        self.fields['creado_por'].empty_label = None
        self.fields['modi_por'].empty_label = None

        hora = datetime.datetime.now()
        self.initial['modi_el'] = hora
        self.fields['modi_el'] = DateTimeField(widget=DateTimePickerInput(format=settings.DATETIME_FORMAT))
        self.fields['creado_el'] = DateTimeField(widget=DateTimePickerInput(format=settings.DATETIME_FORMAT))

        if oficio_id <= 0:
            # print("La hora es: {0} y el oficio es: {1}".format( hora, oficio_id) )
            self.fields['creado_por'].queryset = Usuario.objects.filter(pk=user_id)
            self.initial['creado_el'] = hora
            self.fields['creado_el'] = DateTimeField(widget=DateTimePickerInput(format=settings.DATETIME_FORMAT))
            self.fields['modi_por'].queryset = Usuario.objects.filter(pk=user_id)
        else:
            self.fields['creado_por'].widget = forms.HiddenInput()
            self.fields['creado_el'].widget = forms.HiddenInput()
            self.fields['modi_por'].widget = forms.HiddenInput()
            self.fields['modi_el'].widget = forms.HiddenInput()


        # self.fields['remitente'].widget.attrs['readonly'] = True

    def set_consecutivo(self, consec):
        self.fields['consecutivo'].widget.attrs['readonly'] = False
        self.initial['consecutivo'] = consec
        self.fields['consecutivo'].widget.attrs['readonly'] = False

    def get_consecutivo(self):
        TotalRegistros = OficioEnviado.objects.all()
        if TotalRegistros.count() > 0:
            return OficioEnviado.objects.filter().latest('consecutivo').consecutivo + 1
        else:
            return 1

    def set_remitente(self, remitente):
        self.fields['remitente'].widget.attrs['readonly'] = False
        self.initial['remitente'] = remitente
        self.fields['remitente'].widget.attrs['readonly'] = True

    def get_remitente(self):
        return self.dependencias

    def set_modi_por(self, modi_por):
        self.initial['modi_por'] = modi_por

    def set_modi_el(self, modi_el):
        self.initial['modi_por'] = modi_el




## -------------------------------------------------------------------------------
## MODEL FORM RESPUESTAS
## -------------------------------------------------------------------------------

class OficioEnviadoRespuestaForm(ModelForm):
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
        model = OficioEnviadoRespuestas
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
        super(OficioEnviadoRespuestaForm, self).__init__(*args, **kwargs)
        self.initial['fecha_respuesta'] = self.instance.fecha_respuesta.isoformat()
        print("HA INICIADO BIEN")

    def get_id(self):
        return "{0}".format(self.id)
