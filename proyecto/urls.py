from django.conf.urls.static import static
from django.template.defaulttags import url

import proyecto.reportes.panel_reporte_1
from proyecto.views import oficios_list, oficio_new, oficios_edit, oficios_remove, respuesta_new, \
    oficio_respuestas_list, respuesta_edit, respuesta_remove, oficios_search_list
from siad import settings
from django.urls import path
from .ajax.dependencias import getDependencias
from .reportes.panel_reporte_1 import PDF, reportespecial

urlpatterns = [
    path('oficios_list/<int:tipo_documento>', oficios_list, name='oficios_list'),
    path('oficio_new/<int:tipo_documento>', oficio_new, name='oficio_new'),
    path('oficio_edit/<int:id>/<int:tipo_documento>', oficios_edit, name='oficios_edit'),
    path('oficio_remove/<int:id>/<int:tipo_documento>', oficios_remove, name='oficio_remove'),
    path('oficios_search_list/', oficios_search_list, name='oficios_search_list'),

    path('oficio_respuestas_list/<int:oficio>/<int:tipo_documento>', oficio_respuestas_list, name='oficio_respuestas_list'),
    path('respuesta_new/<int:oficio>', respuesta_new, name='respuesta_new'),
    path('respuesta_edit/<int:id>', respuesta_edit, name='respuesta_edit'),
    path('respuesta_remove/<int:id>', respuesta_remove, name='respuesta_remove'),

    path('getDependencias/', getDependencias, name='/getDependencias'),

    # url("^reportespecial/(?P<mensaje>.*)$/(?P<oficios>.*)$"),
    path('reportespecial/', reportespecial, name='reportespecial'),

    # url(r'^(?P<reportespecial>\w+)/$', reportespecial,),

  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root = settings.MEDIA_ROOT
    )
