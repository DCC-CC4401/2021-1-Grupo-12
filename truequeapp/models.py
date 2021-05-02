from django.db import models
from django.contrib.auth.models import AbstractUser


# El modelo predeterminado de User en Django ya trae los sgtes atributos:
# username, first_name, last_name, email, password, groups, user_permissions, 
# is_staff, is_active, is_superuser, last_login y date_joined.
# Puede ser que debamos ajustar un poco, quizá pedirle un nick específico al usuario
# para que pueda crear su username único.
class Usuario(AbstractUser):
    # Identificación
    id = models.IntegerField(blank=False, primary_key=True)
    rut = models.CharField(max_length=13, blank=True)
    # Contacto
    numero = models.CharField(max_length=13, blank=True)
    red_social = models.URLField(blank=True)
    regiones = [('Arica y Parinacota', 'Arica y Parinacota'), ('Antofagasta', 'Antofagasta'), ('Tarapacá', 'Tarapacá'),
                ('Atacama', 'Atacama'), ('Coquimbo', 'Coquimbo'), ('Valparaíso', 'Valparaíso'),
                ('Región del Libertador Gral. Bernardo O’Higgins', 'Región del Libertador Gral. Bernardo O’Higgins'),
                ('Región del Maule', 'Región del Maule'), ('Región del Biobío', 'Región del Biobío'),
                ('Región de la Araucanía', 'Región de la Araucanía'), ('Región de Los Ríos', 'Región de Los Ríos'),
                ('Región de Los Lagos', 'Región de Los Lagos'),
                ('Región Aisén del Gral. Carlos Ibáñez del Campo', 'Región Aisén del Gral. Carlos Ibáñez del Campo'),
                ('Región de Magallanes y de la Antártíca Chilena', 'Región de Magallanes y de la Antártíca Chilena'),
                ('Región Metropolitana de Santiago', 'Región Metropolitana de Santiago')]
    region = models.CharField(max_length=254, choices=regiones)
    # Seguridad
    correo_respaldo = models.EmailField(max_length=254, blank=True)


class Publicacion(models.Model):

    ########################################################################################

    # Diferentes Estados de un producto a publicar
    NUEVO = "N"
    SEMINUEVO = "SN"
    USADO = "U"
    ESTADOS = [
        (NUEVO, "Nuevo"),
        (SEMINUEVO, "Semi nuevo"),
        (USADO, "Usado"),
    ]

    ########################################################################################

    # Diferentes Categorias a las que puede pertenecer un producto a publicar
    ACCESORIOS = "Ac"
    APARATOS_ELECTRONICOS = "AE"
    AUDIO_FOTO = "AF"
    ARTESANIAS_JOYERIA = "AJ"
    CAMPING = "Cm"
    DEPORTES = "Dp"
    HERRAMIENTAS = "Hr"
    HOGAR_MUEBLES = "HM"
    JUGUETES = "Jg"
    MATERIA_PRIMA = "MP"
    MUSICA_INSTRUMENTOS = "MI"
    LIBROS = "Lb"
    PELICULAS_SERIES = "PS"
    ROPA = "Rp"
    SALUD = "Sl"
    TECNOLOGIA = "Tc"
    VEHICULOS = "Vh"
    OTROS = "Ot"
    CATEGORIAS = [
        (ACCESORIOS, "Accesorios"),
        (APARATOS_ELECTRONICOS, "Aparatos Electronicos"),
        (AUDIO_FOTO, "Audio/Foto"),
        (ARTESANIAS_JOYERIA, "Artesania/Joyeria"),
        (CAMPING, "Camping"),
        (DEPORTES, "Deportes"),
        (HERRAMIENTAS, "Herramientas"),
        (HOGAR_MUEBLES, "Hogar/Muebles"),
        (JUGUETES, "Juguetes"),
        (MATERIA_PRIMA, "Materia prima"),
        (MUSICA_INSTRUMENTOS, "Musica/Instrumentos"),
        (LIBROS, "Libros"),
        (PELICULAS_SERIES, "Peliculas/Series"),
        (ROPA, "Ropa"),
        (SALUD, "Salud"),
        (TECNOLOGIA, "Tecnologia"),
        (VEHICULOS, "Vehiculos"),
        (OTROS, "Otros"),   
        ]
    
    ########################################################################################

    id = models.IntegerField(blank=False, primary_key=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=False)
    estado = models.CharField(max_length=2, blank=False, choices=ESTADOS)
    categoria = models.CharField(max_length=2, blank=False, choices=CATEGORIAS)
    foto_principal = models.ImageField(upload_to='publicaciones/%Y/%m/%d/')
    foto_2 = models.ImageField(upload_to='publicaciones/%Y/%m/%d/')
    foto_3 = models.ImageField(upload_to='publicaciones/%Y/%m/%d/')
    foto_4 = models.ImageField(upload_to='publicaciones/%Y/%m/%d/')
    foto_5 = models.ImageField(upload_to='publicaciones/%Y/%m/%d/')
    cambio = models.CharField(max_length=2, blank=False, choices=CATEGORIAS)
    publicador = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    fecha = models.DateField(blank=False, auto_now=True)


class TruequesAbiertos(models.Model):
    # id = models.IntegerField(blank=False, primary_key=True) produce un error, por mientras dejar asi
    publicacion = models.ForeignKey("Publicacion", on_delete=models.CASCADE)
    interesado = models.ForeignKey("Usuario", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['publicacion', 'interesado'], name='no repetir trueque')
            ]

    def save(self, *args, **kwargs):
        if Publicacion.objects.filter(publicador=self.interesado, categoria=self.publicacion.cambio).count() > 0:
            super().save(*args, **kwargs)