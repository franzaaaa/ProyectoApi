from unicodedata import name
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.conf import settings

import uuid, os

def recipe_image_file_path(instance,filename):
    #Genera path para imagenes
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    
    return os.path.join('uploads/recipe/', filename)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        #Crea y guarda un usuario
        if not email:
            raise ValueError('Users Must Have an Email')
        
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        
        return user
    
    def create_superuser(self, email, password):
        #Crear superuser
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        return user

class User(AbstractBaseUser,PermissionsMixin):
    #Modelo personalizado de Usuario
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_validated = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    
class Ingredient(models.Model):
    #Modelo de Ingrediente
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    #Modelo de receta
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    grupo = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    img = models.ImageField(null=True, upload_to=recipe_image_file_path)
    ingredients = models.ManyToManyField(Ingredient)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.title


class Carrito(models.Model):
    #Modelo de carrito
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Mods(models.Model):
    #Modelo para el registro de Inicios de Sesión
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    date = models.TimeField(auto_now=True, auto_now_add=False)