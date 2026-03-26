from django.contrib import admin
from .models import Usuario, Vehiculo, Evento, Viaje, Plaza, Comentario, Ranking

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Vehiculo)
admin.site.register(Evento)
admin.site.register(Viaje)
admin.site.register(Plaza)
admin.site.register(Comentario)
admin.site.register(Ranking)
