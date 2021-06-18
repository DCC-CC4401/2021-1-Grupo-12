from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE


# El modelo predeterminado de User en Django ya trae los sgtes atributos:
# username, first_name, last_name, email, password, groups, user_permissions, 
# is_staff, is_active, is_superuser, last_login y date_joined.
# Puede ser que debamos ajustar un poco, quizá pedirle un nick específico al usuario
# para que pueda crear su username único.
class Usuario(AbstractUser):
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

    def get_num_mess(self):
        return len(Mensaje.objects.filter(usuario_id=self.id, estado="N").values())


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

    # Estado de la publicación (si fue realizado el trueque entre usuarios, bajado el post, etc)
    ACTIVO = "A"
    ELIMINADO = "E"
    INACTIVO = "I"

    COMPLETADOS = [
        (ACTIVO, "Activo"),
        (ELIMINADO, "Eliminado"),
        (INACTIVO, "Inactivo"),
    ]

    ########################################################################################

    titulo = models.CharField(max_length=200, blank=False)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=2, blank=False, choices=ESTADOS)
    completado = models.CharField(max_length=1, blank=False, choices=COMPLETADOS, default=ACTIVO)
    categoria = models.CharField(max_length=2, blank=False, choices=CATEGORIAS)
    foto_principal = models.ImageField(upload_to='publicaciones/%Y/%m/%d/')
    foto_2 = models.ImageField(upload_to='publicaciones/%Y/%m/%d/')
    foto_3 = models.ImageField(upload_to='publicaciones/%Y/%m/%d/')
    foto_4 = models.ImageField(upload_to='publicaciones/%Y/%m/%d/')
    foto_5 = models.ImageField(upload_to='publicaciones/%Y/%m/%d/')
    cambio = models.CharField(max_length=2, blank=False, choices=CATEGORIAS)
    publicador = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    fecha = models.DateField(blank=False, auto_now=True)

class Trueque(models.Model):
     # Estado del trueque (si fue realizado el trueque entre usuarios, no concretado, etc)
    ABIERTO = "A"
    CONCRETADO = "C"
    FALLIDO = "F"

    ESTADO = [
        (ABIERTO, "Abierto"),
        (CONCRETADO, "Concretado"),
        (FALLIDO, "Fallido"),
    ]

    oferente = models.ForeignKey("Usuario", on_delete=models.CASCADE, related_name='oferente')
    publicacion_oferente = models.ForeignKey("Publicacion", on_delete=models.CASCADE, related_name='publicacion_oferente')

    demandante = models.ForeignKey("Usuario", on_delete=models.CASCADE, related_name='demandante')
    publicacion_demandante = models.ForeignKey("Publicacion", on_delete=models.CASCADE, related_name='publicacion_demandante')

    estado = models.CharField(max_length=1, blank=False, choices=ESTADO, default=ABIERTO)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['publicacion_oferente', 'publicacion_demandante'], name='no repetir trueque')
            ]

    def save(self, *args, **kwargs):
        if Publicacion.objects.filter(publicador=self.demandante, categoria=self.publicacion_oferente.cambio).count() > 0:
            super().save(*args, **kwargs)

class Mensaje(models.Model):
    CALIFICAR = "C"
    REVISAR = "R"
    ACEPTAR = "A"
    TIPO = [
        (CALIFICAR, "calificar"),
        (REVISAR, "revisar"),
        (ACEPTAR, "aceptar"),
    ]

    VISTO = "V"
    NOVISTO = "N"
    ESTADO = [
        (VISTO, "Visto"),
        (NOVISTO, "No visto"),
    ]

    usuario = models.ForeignKey("Usuario", on_delete=CASCADE)
    trueque_asoc = models.ForeignKey("Trueque", on_delete=CASCADE)
    fecha_de_envio = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=1, blank=False, choices=TIPO)
    estado = models.CharField(max_length=1, blank=False, choices=ESTADO, default=NOVISTO)

    class Meta:
        # sort by "fecha" in descending order unless
        # overridden in the query with order_by()
        ordering = ['-fecha_de_envio']
