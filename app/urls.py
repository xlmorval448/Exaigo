from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .models import Usuario, Vehiculo, Evento, Viaje, Plaza, Comentario, Ranking
from .views import UsuarioViewSet, VehiculoViewSet, EventoViewSet, ViajeViewSet, PlazaViewSet, ComentarioViewSet, RankingViewSet

#API

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'vehiculos', VehiculoViewSet)
router.register(r'eventos', EventoViewSet)
router.register(r'viajes', ViajeViewSet)
router.register(r'plazas', PlazaViewSet)
router.register(r'comentarios', ComentarioViewSet)
router.register(r'rankings', RankingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]