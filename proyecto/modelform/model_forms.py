from django.forms import ModelForm, TextInput, DateInput, ModelChoiceField, DateField, Textarea, widgets, Select
from django import forms

from proyecto.models import Oficio, Dependencia, Subdireccione, Respuestas
from siad import settings

## -------------------------------------------------------------------------------
## MODEL FORM OFICIOS
## -------------------------------------------------------------------------------

class OficioForm(ModelForm):
    dir_remitente = ModelChoiceField(label='Dependencia', queryset=Dependencia.objects.all())
    recibe = ModelChoiceField(label='Recibe', queryset=Subdireccione.objects.all())

    fecha_documento = DateField(widget=forms.widgets.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
                           input_formats=settings.DATE_INPUT_FORMATS)
    fecha_captura = DateField(widget=forms.widgets.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
                           input_formats=settings.DATE_INPUT_FORMATS)
    fecha_respuesta = DateField(widget=forms.widgets.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
                           input_formats=settings.DATE_INPUT_FORMATS)
    fecha_recibido = DateField(widget=forms.widgets.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
                           input_formats=settings.DATE_INPUT_FORMATS)

    class DateInput(forms.DateInput):
        input_type = 'date'

    class Meta:
        model = Oficio
        fields = '__all__'
        exclude = ['respuestas', 'archivo_datetime', 'creado_por', 'creado_el', 'modi_por', 'modi_el']
        widgets = {
            'consecutivo': TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'remitente': TextInput(attrs={'class': 'form-control'}),
            'recibe': TextInput(attrs={'class': 'form-control'}),
            'instrucciones': Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 80}),
            'asunto': Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 80}),
        },
        labels = {
            "anno": "Año",
            "tipo_documento": "Tipo de Oficio",
            "dir_remitente": "dir_remitente(*)",
        }


    def __init__(self, *args, **kwargs):
        super(OficioForm, self).__init__(*args, **kwargs)

        self.initial['fecha_documento'] = self.instance.fecha_documento.isoformat()
        self.initial['fecha_captura'] = self.instance.fecha_captura.isoformat()
        self.initial['fecha_respuesta'] = self.instance.fecha_respuesta.isoformat()
        self.initial['fecha_recibido'] = self.instance.fecha_recibido.isoformat()

        self.fields['dir_remitente'].queryset = Dependencia.objects.all()
        self.fields['recibe'].queryset = Subdireccione.objects.all()
        self.fields['tipo_documento'].widget = forms.HiddenInput()


    def set_consecutivo(self, consec):
        self.fields['consecutivo'].widget.attrs['readonly'] = False
        self.initial['consecutivo'] = consec
        self.fields['consecutivo'].widget.attrs['readonly'] = True

    def get_consecutivo(self):
        return self.consecutivo



    def set_tipo_documento(self, td):
        self.initial['tipo_documento'] = td

    def get_tipo_documento(self):
        return self.tipo_documento








## -------------------------------------------------------------------------------
## MODEL FORM RESPUESTAS
## -------------------------------------------------------------------------------

class RespuestaForm(ModelForm):
    fecha_respuesta = DateField(widget=forms.widgets.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
                           input_formats=settings.DATE_INPUT_FORMATS)

    class DateInput(forms.DateInput):
        input_type = 'date'

    class Meta:
        model = Respuestas
        fields = '__all__'
        exclude = ['archivo_datetime', 'creado_por', 'creado_el', 'modi_por', 'modi_el']
        widgets = {
            'respuesta': Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 80}),
        },
        labels = {
            "fecha_respuesta": "Fecha de Respuesta",
            "respuesta": "Respuesta",
        }


    def __init__(self, *args, **kwargs):
        super(RespuestaForm, self).__init__(*args, **kwargs)
        self.initial['fecha_respuesta'] = self.instance.fecha_respuesta.isoformat()
