## -------------------------------------------------------------------------------
## MODEL FORM OFICIOS
## -------------------------------------------------------------------------------
import datetime

from bootstrap_datepicker_plus.widgets import DatePickerInput, DateTimePickerInput
from django import forms
from django.forms import ModelForm, ModelChoiceField, DateField, TextInput, Textarea, Select, DateTimeField
from django.shortcuts import get_object_or_404

from home.models import Usuario
from oficiosenviados.models import OficioEnviado, OficioEnviadoRespuestas
from proyecto.models import Dependencia, UnidadAdministrativa, Subdireccione
from siad import settings


class OficioEnviadoForm(ModelForm):
    remitente = ModelChoiceField(label='Remitente', queryset=Subdireccione.objects.all())
    unidad_administrativa = ModelChoiceField(label='Unidad Administrativa', queryset=UnidadAdministrativa.objects.all())

    fecha_oficio = DateField(widget=DatePickerInput(format=settings.DATE_FORMAT))

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
        }

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        oficio_id = kwargs.pop('oficioenviado_id', None)
        super(OficioEnviadoForm, self).__init__(*args, **kwargs)
        if oficio_id > 0:
            Ofi = get_object_or_404(OficioEnviado, pk=oficio_id)
            ua = UnidadAdministrativa.objects.filter(id=Ofi.unidad_administrativa_id)
        else:
            ua = UnidadAdministrativa.objects.all()
        self.fields['unidad_administrativa'].queryset = ua
        self.fields['unidad_administrativa'].empty_label = None
        self.fields['remitente'].queryset = Subdireccione.objects.all()
        self.fields['creado_por'].empty_label = None
        self.fields['modi_por'].empty_label = None

        hora = datetime.datetime.now()
        self.initial['modi_el'] = hora
        self.fields['modi_el'] = DateTimeField(widget=DateTimePickerInput(format=settings.DATETIME_FORMAT))
        self.fields['creado_el'] = DateTimeField(widget=DateTimePickerInput(format=settings.DATETIME_FORMAT))

        if oficio_id <= 0:
            self.fields['creado_por'].queryset = Usuario.objects.filter(pk=user_id)
            self.initial['creado_el'] = hora
            self.fields['creado_el'] = DateTimeField(widget=DateTimePickerInput(format=settings.DATETIME_FORMAT))
            self.fields['modi_por'].queryset = Usuario.objects.filter(pk=user_id)
        else:
            self.fields['unidad_administrativa'].widget = forms.HiddenInput()
            self.fields['creado_por'].widget = forms.HiddenInput()
            self.fields['creado_el'].widget = forms.HiddenInput()
            self.fields['modi_por'].widget = forms.HiddenInput()
            self.fields['modi_el'].widget = forms.HiddenInput()

    def set_consecutivo(self, consec):
        if consec is None:
            consec = self.get_consecutivo()
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
