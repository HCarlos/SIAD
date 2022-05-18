from datetime import datetime, timezone, timedelta

from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.forms import ModelForm, TextInput, DateInput, ModelChoiceField, Textarea, widgets, Select
from django import forms

from proyecto.models import Oficio, Dependencia, Subdireccione, Respuestas
from siad import settings
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
## -------------------------------------------------------------------------------
## MODEL FORM OFICIOS
## -------------------------------------------------------------------------------

class OficioForm(ModelForm):
    dir_remitente = ModelChoiceField(label='Dependencia', queryset=Dependencia.objects.all())
    recibe = ModelChoiceField(label='Recibe', queryset=Subdireccione.objects.all())


    # fecha_documento = DateField(widget=forms.widgets.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
    #                        input_formats=settings.DATE_INPUT_FORMATS)
    # fecha_captura = DateField(widget=forms.widgets.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
    #                        input_formats=settings.DATE_INPUT_FORMATS )
    # fecha_respuesta = DateField(widget=forms.widgets.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
    #                        input_formats=settings.DATE_INPUT_FORMATS)
    # fecha_recibido = DateField(widget=forms.widgets.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
    #                        input_formats=settings.DATE_INPUT_FORMATS)

    fecha_documento = DateField(widget=DatePickerInput(format=settings.DATE_FORMAT))
    fecha_captura   = DateField(widget=DatePickerInput(format=settings.DATE_FORMAT))
    fecha_respuesta = DateField(widget=DatePickerInput(format=settings.DATE_FORMAT))
    fecha_recibido  = DateField(widget=DatePickerInput(format=settings.DATE_FORMAT))

    instrucciones = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'cols': 5}))

    class DateInput(forms.DateInput):
        input_type = 'date'

    class Meta:
        model = Oficio
        fields = '__all__'
        exclude = ['respuestas', 'archivo_datetime', 'creado_por', 'creado_el', 'modi_por', 'modi_el']
        widgets = {
            'remitente': TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'recibe': TextInput(attrs={'class': 'form-control'}),
            'instrucciones': Textarea(attrs={'class': 'form-control', 'rows': 45, 'cols': 80}),
            'asunto': Textarea(attrs={'class': 'form-control', 'rows': 45, 'cols': 80}),
          },
        # 'consecutivo': TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
        labels = {
            "anno": "Año",
            "tipo_documento": "Tipo de Oficio",
            "dir_remitente": "dir_remitente(*)",
        }


    def __init__(self, *args, **kwargs):
        super(OficioForm, self).__init__(*args, **kwargs)

        # self.initial['fecha_documento'] = self.instance.fecha_documento.isoformat()
        # self.initial['fecha_captura'] = self.instance.fecha_captura.isoformat()
        # self.initial['fecha_respuesta'] = self.instance.fecha_respuesta.isoformat()
        # self.initial['fecha_recibido'] = self.instance.fecha_recibido.isoformat()
        # self.fecha_captura = DateField(initial=datetime.today().strftime('%d-%m-%Y') )

        self.fields['dir_remitente'].queryset = Dependencia.objects.all()
        self.fields['recibe'].queryset = Subdireccione.objects.all()
        self.fields['tipo_documento'].widget = forms.HiddenInput()

        self.fields['remitente'].widget.attrs['readonly'] = True

    def set_consecutivo(self, consec):
        # self.fields['consecutivo'].widget.attrs['readonly'] = False
        # self.initial['consecutivo'] = consec
        # self.fields['consecutivo'].widget.attrs['readonly'] = True

        self.fields['consecutivo'].widget.attrs['readonly'] = False

        self.initial['consecutivo'] = consec
        # self.fields['consecutivo'] = "%s" % consec

        # self.fields['consecutivo'].widget.attrs['readonly'] = True
        self.fields['consecutivo'].widget.attrs['readonly'] = False

    def get_consecutivo(self, TD):
        return Oficio.objects.filter(tipo_documento=TD).latest('consecutivo').consecutivo + 1
        # self.consecutivo
        # return self.fields['consecutivo']

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
