from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

class ProvinciaOpcion(models.TextChoices):
    ALAVA = 'VI', 'Álava'
    ALBACETE = 'AB', 'Albacete'
    ALICANTE = 'A', 'Alicante'
    ALMERIA = 'AL', 'Almería'
    AVILA = 'AV', 'Ávila'
    BADAJOZ = 'BA', 'Badajoz'
    BALEARES = 'PM', 'Baleares'
    BARCELONA = 'B', 'Barcelona'
    BURGOS = 'BU', 'Burgos'
    CACERES = 'CC', 'Cáceres'
    CADIZ = 'CA', 'Cádiz'
    CASTELLON = 'CS', 'Castellón'
    CIUDAD_REAL = 'CR', 'Ciudad Real'
    CORDOBA = 'CO', 'Córdoba'
    A_CORUNA = 'C', 'A Coruña'
    CUENCA = 'CU', 'Cuenca'
    GIRONA = 'GI', 'Girona'
    GRANADA = 'GR', 'Granada'
    GUADALAJARA = 'GU', 'Guadalajara'
    GIPUZKOA = 'SS', 'Gipuzkoa'
    HUELVA = 'H', 'Huelva'
    HUESCA = 'HU', 'Huesca'
    JAEN = 'J', 'Jaén'
    LEON = 'LE', 'León'
    LLEIDA = 'L', 'Lleida'
    LA_RIOJA = 'LO', 'La Rioja'
    LUGO = 'LU', 'Lugo'
    MADRID = 'M', 'Madrid'
    MALAGA = 'MA', 'Málaga'
    MURCIA = 'MU', 'Murcia'
    NAVARRA = 'NA', 'Navarra'
    OURENSE = 'OU', 'Ourense'
    ASTURIAS = 'O', 'Asturias'
    PALENCIA = 'P', 'Palencia'
    LAS_PALMAS = 'GC', 'Las Palmas'
    PONTEVEDRA = 'PO', 'Pontevedra'
    SALAMANCA = 'SA', 'Salamanca'
    SANTA_CRUZ_DE_TENERIFE = 'TF', 'Santa Cruz de Tenerife'
    CANTABRIA = 'S', 'Cantabria'
    SEGOVIA = 'SG', 'Segovia'
    SEVILLA = 'SE', 'Sevilla'
    SORIA = 'SO', 'Soria'
    TARRAGONA = 'T', 'Tarragona'
    TERUEL = 'TE', 'Teruel'
    TOLEDO = 'TO', 'Toledo'
    VALENCIA = 'V', 'Valencia'
    VALLADOLID = 'VA', 'Valladolid'
    BIZKAIA = 'BI', 'Bizkaia'
    ZAMORA = 'ZA', 'Zamora'
    ZARAGOZA = 'Z', 'Zaragoza'
    CEUTA = 'CE', 'Ceuta'
    MELILLA = 'ML', 'Melilla'

class MesOpcion(models.TextChoices):
    ENERO = '1', 'Enero'
    FEBRERO = '2', 'Febrero'
    MARZO = '3', 'Marzo'
    ABRIL = '4', 'Abril'
    MAYO = '5', 'Mayo'
    JUNIO = '6', 'Junio'
    JULIO = '7', 'Julio'
    AGOSTO = '8', 'Agosto'
    SEPTIEMBRE = '9', 'Septiembre'
    OCTUBRE = '10', 'Octubre'
    NOVIEMBRE = '11', 'Noviembre'
    DICIEMBRE = '12', 'Diciembre'

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=20)
    dni = models.CharField(max_length=9, unique=True)
    fotoPerfil = models.ImageField(upload_to="perfiles/", null=True, blank=True)
    verificado = models.BooleanField(default=False)
    puntosMovilidad = models.IntegerField(default=0)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    esConductor = models.BooleanField(default=False)

    @property
    def valoracion_media(self):
        media = self.comentariosRecibidos.aggregate(Avg('estrellas'))['estrellas__avg']
        return round(media, 1) if media else 0.0

    def __str__(self):
        return str(self.username)

class Vehiculo(models.Model):
    matricula = models.CharField(max_length=15, primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="vehiculos")
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    anio = models.PositiveIntegerField()
    consumoMedio = models.FloatField(validators=[MinValueValidator(0.1)])
    plazasTotales = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.matricula})"

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    fecha = models.DateTimeField()
    lugar = models.CharField(max_length=200)

    def __str__(self):
        return str(self.nombre)

class Viaje(models.Model):
    class EstadoViaje(models.TextChoices):
        DISPONIBLE = 'DI', 'Disponible'
        COMPLETO = 'CO', 'Completo'
        FINALIZADO = 'FI', 'Finalizado'

    conductor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="viajesOfrecidos")
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.SET_NULL, null=True, blank=True, related_name="viajes")

    origen = models.CharField(max_length=100)
    latitud_origen = models.FloatField(null=True, blank=True)
    longitud_origen = models.FloatField(null=True, blank=True)

    destino = models.CharField(max_length=100)
    latitud_destino = models.FloatField(null=True, blank=True)
    longitud_destino = models.FloatField(null=True, blank=True)

    fechaSalida = models.DateTimeField()
    distanciaKm = models.FloatField(validators=[MinValueValidator(0.1)])
    precioTotalTrayecto = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.CharField(max_length=2, choices=EstadoViaje.choices, default=EstadoViaje.DISPONIBLE)

    def __str__(self):
        return f"Viaje de {self.conductor.username} el {self.fechaSalida.strftime('%Y-%m-%d %H:%M')}"

class Plaza(models.Model):
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, related_name="reservas")
    pasajero = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="misPlazas")
    pagado = models.BooleanField(default=False)
    fechaPago = models.DateTimeField(auto_now_add=True)

class Comentario(models.Model):
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="comentariosHechos")
    conductor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="comentariosRecibidos")
    puntuacion = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reseña a {self.conductor.username} por viaje {self.viaje.id}"

class Ranking(models.Model):
    conductor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    provincia = models.CharField(max_length=2, choices=ProvinciaOpcion.choices)
    mes = models.CharField(max_length=2, choices=MesOpcion.choices)
    anio = models.PositiveIntegerField()
    puntos = models.IntegerField(default=0)
    posicion = models.PositiveIntegerField()
    top1 = models.IntegerField(default=0)
    top2 = models.IntegerField(default=0)
    top3 = models.IntegerField(default=0)