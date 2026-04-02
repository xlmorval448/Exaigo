from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.urls import reverse_lazy
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Usuario, Vehiculo, Evento, Viaje, Plaza, Comentario, Ranking
from .serializers import UsuarioSerializer, VehiculoSerializer, EventoSerializer, ViajeSerializer, PlazaSerializer, ComentarioSerializer, RankingSerializer
from .forms import UsuarioRegistroForm, UsuarioForm, VehiculoForm
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
    form_class = UsuarioRegistroForm
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
    success_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user == self.get_object()

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        password = request.POST.get('password_confirm')

        if user.check_password(password):
            messages.success(request, "Cuenta eliminada correctamente.")
            return super().post(request, *args, **kwargs)
        else:
            messages.error(request, "La contraseña introducida es incorrecta.")
            return redirect('usuario_editar', pk=user.pk)

    def get(self, request, *args, **kwargs):
        return redirect('usuario_editar', pk=self.kwargs['pk'])

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para eliminar este usuario.")
        return redirect("usuarios_lista")

    def get_success_url(self):
        messages.success(self.request, "Usuario Eliminado Correctamente.")
        return super().get_success_url()

class VehiculoCreateView(LoginRequiredMixin, CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'app/vehiculo_crear.html'

    def form_valid(self, form):
        form.instance.usuario = self.request.user

        user = self.request.user
        user.esConductor = True
        user.save()

        messages.success(self.request, "Vehículo registrado. Ahora eres conductor.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('usuario_detalle', kwargs={'pk': self.request.user.pk})

class VehiculoDetailView(LoginRequiredMixin, DetailView):
    model = Vehiculo
    template_name = 'app/vehiculo_detalle.html'
    context_object_name = "vehiculo"
    pk_url_kwarg = 'matricula'

class VehiculoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Vehiculo
    template_name = 'app/vehiculo_eliminar.html'
    pk_url_kwarg = 'matricula'

    def test_func(self):
        return self.request.user == self.get_object().usuario

    def get(self, request, *args, **kwargs):
        return redirect('vehiculo_detalle', pk=self.kwargs['pk'], matricula=self.kwargs['matricula'])

    def form_valid(self, form):
        user = self.request.user
        user.esConductor = False
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Vehículo eliminado. Ya no eres conductor.")
        return reverse_lazy('usuario_detalle', kwargs={'pk': self.request.user.pk})