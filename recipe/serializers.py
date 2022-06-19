from dataclasses import fields
from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers
from yaml import serialize
from core import models
from user.serializers import UserSerializer
from core.models import Carrito, User, Product


        
class IngredientSerializer(serializers.ModelSerializer):
    #Serializador para modelo Ingrediente
    class Meta:
        model = models.Ingredient
        fields = ['id','name']
  
class IngredientDetailSerializer(IngredientSerializer):
    #Serializamos los detalles de ingrediente
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
      
        
class ProductSerializer(serializers.ModelSerializer):
    #Serializador para modelo Receta
    ingredients = IngredientSerializer(read_only=True, many=True)
    id = serializers.IntegerField()
    
    class Meta:
        model = models.Product
        fields = ('id', 'title', 'ingredients', 'cantidad', 'descripcion', 'price', 'img',)
        
        
class ProductDetailSerializer(ProductSerializer):
    #Serializamos los detalles del producto
    ingredients = IngredientSerializer(read_only=True, many=True)
    

class ProductImageSerializer(serializers.ModelSerializer):
    #Serializador de imagen
    class Meta:
        model = models.Product
        fields = ('id','img')


class CarritoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = ProductSerializer()

    def create(self, validated_data):
        us = User.objects.get(email=validated_data['user'])
        pr = Product.objects.get(id=validated_data['product']['id'])
        return Carrito.objects.create(user=us,product=pr)

    #Serializador de imagen
    class Meta:
        model = models.Carrito
        fields = ('user','product')
        depth = 1


class ModsSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.Mods
        fields = ('user','date')
