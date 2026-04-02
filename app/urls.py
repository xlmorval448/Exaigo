from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .models import Usuario, Vehiculo, Evento, Viaje, Plaza, Comentario, Ranking
from .views import UsuarioViewSet, VehiculoViewSet, EventoViewSet, ViajeViewSet, PlazaViewSet, ComentarioViewSet, RankingViewSet

# API

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

# APP

urlpatterns += [
    path('inicio/', views.InicioView.as_view(), name='inicio'),
    path('usuario/nuevo/', views.UsuarioCreateView.as_view(), name='usuario_crear'),
    path('usuario/<int:pk>/', views.UsuarioDetailView.as_view(), name='usuario_detalle'),
    path('usuario/<int:pk>/editar/', views.UsuarioUpdateView.as_view(), name='usuario_editar'),
    path('usuario/<int:pk>/borrar/', views.UsuarioDeleteView.as_view(), name='usuario_borrar'),
    path('usuario/<int:pk>/vehiculo/nuevo/', views.VehiculoCreateView.as_view(), name='vehiculo_crear'),
    path('usuario/<int:pk>/vehiculo/<str:matricula>/detalle/', views.VehiculoDetailView.as_view(), name='vehiculo_detalle'),
    path('usuario/<int:pk>/vehiculo/<str:matricula>/eliminar/', views.VehiculoDeleteView.as_view(), name='vehiculo_eliminar'),
]