from django.contrib import admin

from proyecto.models import Dependencia, Subdireccione, UnidadMedida, Oficio, Evento, Respuestas

admin.site.register(Dependencia)
admin.site.register(Subdireccione)
admin.site.register(UnidadMedida)
# admin.site.register(OficioConsulta)
admin.site.register(Oficio)
admin.site.register(Respuestas)
admin.site.register(Evento)
