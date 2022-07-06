from django.contrib import admin

from oficiosenviados.models import OficioEnviado
from proyecto.models import Dependencia, Subdireccione, UnidadMedida, Oficio, Evento, Respuestas, UnidadAdministrativa

admin.site.register(Dependencia)
admin.site.register(Subdireccione)
admin.site.register(UnidadMedida)
admin.site.register(UnidadAdministrativa)
admin.site.register(Oficio)
admin.site.register(OficioEnviado)
admin.site.register(Respuestas)
admin.site.register(Evento)
