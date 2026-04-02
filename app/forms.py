from django import forms
from .models import Usuario, Vehiculo, Evento, Viaje, Plaza, Comentario, Ranking
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

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