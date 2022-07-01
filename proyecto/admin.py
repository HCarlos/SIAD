from django.contrib import admin

from proyecto.models import Dependencia, Subdireccione, UnidadMedida, Oficio, Evento, Respuestas, UnidadAdministrativa

admin.site.register(Dependencia)
admin.site.register(Subdireccione)
admin.site.register(UnidadMedida)
admin.site.register(UnidadAdministrativa)
admin.site.register(Oficio)
admin.site.register(Respuestas)
admin.site.register(Evento)
