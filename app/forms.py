from django import forms
from .models import Usuario, Vehiculo, Evento, Viaje, Plaza, Comentario, Ranking
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm


class UsuarioRegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'nombre', 'apellidos', 'dni', 'telefono', 'fechaNacimiento', 'fotoPerfil']
        widgets = {
            'fechaNacimiento': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'nombre', 'apellidos', 'fechaNacimiento', 'dni', 'telefono', 'fotoPerfil']
        widgets = {
            'fechaNacimiento': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuario.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso por otra persona.")
        return username

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['matricula', 'marca', 'modelo', 'color', 'anio', 'consumoMedio', 'plazasTotales', 'foto']
        widgets = {
            'anio': forms.NumberInput(attrs={'min': 1900, 'max': 2026}),
            'consumoMedio': forms.NumberInput(attrs={'step': 0.1}),
        }

    def clean_matricula(self):
        matricula = self.cleaned_data.get('matricula').upper()
        if Vehiculo.objects.filter(matricula=matricula).exists():
            raise forms.ValidationError("Ya existe un vehículo registrado con esta matrícula.")
        return matricula