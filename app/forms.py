from django import forms
from .models import Usuario, Vehiculo, Evento, Viaje, Plaza, Comentario, Ranking
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'nombre', 'apellidos', 'fechaNacimiento', 'dni', 'telefono', 'fotoPerfil']

        widgets = {
            'fechaNacimiento': forms.DateInput(attrs={'type': 'date'})
        }