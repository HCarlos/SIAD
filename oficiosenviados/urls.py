from django.conf.urls.static import static
from django.template.defaulttags import url

import proyecto.reportes.panel_reporte_1
from oficiosenviados.views import OficioEnviados_list, OficioEnviado_new, OficioEnviados_edit, OficioEnviados_remove, \
    OficioEnviados_search_data_list, OficioEnviado_respuestas_list, oficioenviado_respuesta_new, \
    oficioenviado_respuesta_edit, oficioenviado_respuesta_remove
from proyecto.views import oficios_list, oficio_new, oficios_edit, oficios_remove, respuesta_new, \
    oficio_respuestas_list, respuesta_edit, respuesta_remove, oficios_search_list, oficios_search_data_list
from siad import settings
from django.urls import path
from proyecto.ajax.dependencias import getDependencias
from proyecto.reportes.panel_reporte_1 import PDF, reportespecial

# path('oficioenviados_search_list/', oficios_search_list, name='oficios_search_list'),

urlpatterns = [
    path('oficiosenviados_list', OficioEnviados_list, name='oficiosenviados_list'),
    path('oficioenviado_new', OficioEnviado_new, name='oficioenviado_new'),
    path('oficioenviado_edit/<int:id>', OficioEnviados_edit, name='oficioenviado_edit'),
    path('oficioenviado_remove/<int:id>', OficioEnviados_remove, name='oficioenviado_remove'),
    path('oficioenviados_search_data_list', OficioEnviados_search_data_list, name='oficioenviados_search_data_list'),

    path('oficioenviado_respuestas_list/<int:oficio>', OficioEnviado_respuestas_list, name='oficioenviado_respuestas_list'),
    path('oficioenviado_respuesta_new/<int:oficio>', oficioenviado_respuesta_new, name='oficioenviado_respuesta_new'),
    path('oficioenviado_respuesta_edit/<int:id>', oficioenviado_respuesta_edit, name='oficioenviado_respuesta_edit'),
    path('oficioenviado_respuesta_remove/<int:id>', oficioenviado_respuesta_remove, name='oficioenviado_respuesta_remove'),

  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root = settings.MEDIA_ROOT
    )
