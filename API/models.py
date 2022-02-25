from django.db import models

# Create your models here.
class Roles(models.Model):
    nombre = models.CharField(max_length=15)

class Usuario(models.Model):
    dni = models.CharField(max_length=20, unique=True)
    apellidos = models.CharField(max_length=35)
    nombres = models.CharField(max_length=35)
    hobbies = models.TextField(max_length=200)
    email = models.EmailField(max_length=35, unique=True)
    password = models.CharField(max_length=200)
    role = models.ForeignKey(Roles, null=False, blank=False, on_delete=models.CASCADE)
    tipo_dni = models.CharField(max_length=20, default='dni')
    is_anonymous=models.BooleanField(default=False)
    is_authenticated=models.BooleanField(default=False)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []