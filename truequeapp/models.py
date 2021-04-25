from django.db import models
from django.contrib.auth.models import AbstractUser

# El modelo predeterminado de User en Django ya trae los sgtes atributos:
# username, first_name, last_name, email, password, groups, user_permissions, 
# is_staff, is_active, is_superuser, last_login y date_joined.
# Puede ser que debamos ajustar un poco, quizá pedirle un nick específico al usuario
# para que pueda crear su username único.
class User(AbstractUser):
    nombre = models.CharField(max_length=32)
    apellido = models.CharField(max_length=48)
    rut = models.CharField(max_length=13, default="")
    # foto = models.CharField(default="")
    numero = models.CharField(max_length=13, default="")
    red_social = models.URLField()
    regiones = [('Arica y Parinacota', 'Arica y Parinacota'), ('Antofagasta', 'Antofagasta'), ('Tarapacá', 'Tarapacá'),
     ('Atacama', 'Atacama'), ('Coquimbo', 'Coquimbo'), ('Valparaíso', 'Valparaíso'),
     ('Región del Libertador Gral. Bernardo O’Higgins', 'Región del Libertador Gral. Bernardo O’Higgins'),
     ('Región del Maule', 'Región del Maule'), ('Región del Biobío', 'Región del Biobío'),
     ('Región de la Araucanía', 'Región de la Araucanía'), ('Región de Los Ríos', 'Región de Los Ríos'),
     ('Región de Los Lagos', 'Región de Los Lagos'),
     ('Región Aisén del Gral. Carlos Ibáñez del Campo', 'Región Aisén del Gral. Carlos Ibáñez del Campo'), 
     ('Región de Magallanes y de la Antártíca Chilena', 'Región de Magallanes y de la Antártíca Chilena'),
     ('Región Metropolitana de Santiago', 'Región Metropolitana de Santiago')]
    region = models.CharField(max_length=200, choices=regiones)
    correo_respaldo = models.EmailField(max_length=254)