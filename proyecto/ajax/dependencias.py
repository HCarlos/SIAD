from django.core import serializers
from django.http import JsonResponse

from proyecto.models import Dependencia

def llenar_dependencias(request):
    dependencias = Dependencia.objects.all()
    options = '<option value="" selected="selected">---------</option>'
    for dependencia in dependencias:
        options += '<option value="%s" titular="%s">%s</option>' % (
            dependencia.pk,
            dependencia.dependencia,
            dependencia.titutlar
        )
    response = {}
    response['dependencias'] = options
    return JsonResponse(response)

def getDependencias(request):
    response = {}
    response['dependencia']={}
    if request.method == 'POST':
        Id = request.POST['dir_remitente']
        dependencia = Dependencia.objects.filter(pk=Id).get()
        if dependencia:
            response['dependencia'] = serializers.serialize("json",dependencia)
    return JsonResponse(response)
