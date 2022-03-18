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
    if request.method == 'POST':
        Id = request.POST.get('dir_remitente')
        # print(Id)
        dependencia = Dependencia.objects.filter(pk=Id).get()
        if dependencia:
            response = {
                'id': dependencia.pk,
                'dependencia': dependencia.dependencia,
                'titular':  '%s %s %s' % (dependencia.titular.ap_paterno, dependencia.titular.ap_materno, dependencia.titular.nombre),
            }

    return JsonResponse(response)
