from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.urls import reverse_lazy
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Usuario, Vehiculo, Evento, Viaje, Plaza, Comentario, Ranking
from .serializers import UsuarioSerializer, VehiculoSerializer, EventoSerializer, ViajeSerializer, PlazaSerializer, ComentarioSerializer, RankingSerializer
from .forms import UsuarioForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

#API

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super(VehiculoViewSet, self).get_permissions()

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAdminUser]

class ViajeViewSet(viewsets.ModelViewSet):
    queryset = Viaje.objects.all()
    serializer_class = ViajeSerializer
    permission_classes = [IsAdminUser]

class PlazaViewSet(viewsets.ModelViewSet):
    queryset = Plaza.objects.all()
    serializer_class = PlazaSerializer
    

class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    permission_classes = [IsAdminUser]

class RankingViewSet(viewsets.ModelViewSet):
    queryset = Ranking.objects.all()
    serializer_class = RankingSerializer
    permission_classes = [IsAdminUser]

# APP

class InicioView(LoginRequiredMixin, ListView):
    template_name = 'app/inicio.html'
    model = Viaje
    context_object_name = "viajes"

class UsuarioCreateView(CreateView):
    template_name = 'app/usuario_crear.html'
    model = Usuario
    form_class = UsuarioForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, "Usuario Creado Correctamente.")
        return super().form_valid(form)

class UsuarioDetailView(LoginRequiredMixin, DetailView):
    template_name = 'app/usuario_detalle.html'
    model = Usuario
    context_object_name = "usuario"

class UsuarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'app/usuario_editar.html'
    model = Usuario
    form_class = UsuarioForm
    context_object_name = "usuario"

    def test_func(self):
        return self.request.user == self.get_object() or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para editar este usuario.")
        return redirect("usuarios_lista")

    def get_success_url(self):
        messages.success(self.request, "Cambios Guardados Correctamente.")
        return reverse_lazy('usuario_detalle', kwargs={'pk': self.object.pk})

class UsuarioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Usuario
    success_url = reverse_lazy('logout')

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para eliminar este usuario.")
        return redirect("usuarios_lista")

    def get_success_url(self):
        messages.success(self.request, "Usuario Eliminado Correctamente.")
        return super().get_success_url()
