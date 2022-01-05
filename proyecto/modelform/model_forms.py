import datetime

from django.forms import ModelForm, TextInput, DateInput, ModelChoiceField, DateField, Textarea

from proyecto.models import Oficio, Dependencia


class OficioForm(ModelForm):

    dir_remitente= ModelChoiceField(label='Dependencia', queryset=Dependencia.objects.all())

    class Meta:
        model = Oficio
        fields = '__all__'
        exclude = ['archivo_datetime', 'creado_por', 'creado_el', 'modi_por', 'modi_el']
        widgets = {
            'fecha_documento': TextInput(attrs={'type': 'date', 'class': 'form-input'}),
            'fecha_captura': TextInput(attrs={'type': 'date', 'class': 'form-input'}),
            'fecha_respuesta': TextInput(attrs={'type': 'date', 'class': 'form-input'}),
            'asunto': Textarea(attrs={'class': 'form-input', 'rows': 5, 'cols': 80}),
        }

    def __init__(self, *args, **kwargs):
        super(OficioForm, self).__init__(*args, **kwargs)
        self.fields['dir_remitente'].queryset = Dependencia.objects.all()
