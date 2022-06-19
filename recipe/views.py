from django.shortcuts import render
from django.http import JsonResponse
from html5lib import serialize
from rest_framework.response import Response
from rest_framework import generics, authentication, permissions, authtoken
from core.models import Ingredient, User, Product, Carrito, Mods
from recipe import serializers
from user.serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework import viewsets, mixins, status

from rest_framework.settings import api_settings
from rest_framework.decorators import action
from django.conf import settings


class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = serializers.CarritoSerializer
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        #Crear nuevo Ingrediente
        prod = Product.objects.get(id=serializer.validated_data['product']['id'])
        prod.cantidad = prod.cantidad - 1
        prod.save()
        serializer.save(user=self.request.user)



class ModsViewSet(viewsets.ModelViewSet):
    queryset = Mods.objects.all()
    serializer_class = serializers.ModsSerializer
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        #Crear nuevo Ingrediente
        print("fdsfs")
        serializer.save(user=self.request.user)      
        
class IngredientViewSet(viewsets.ModelViewSet):
    #Manejar ingredientes en base de datos
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    
    def get_queryset(self):
        #Retornamos objetos para el usuario autenticado
        return self.queryset
    
    def perform_create(self, serializer):
        #Crear nuevo Ingrediente
        serializer.save(user=self.request.user)
        
    def perform_update(self, serializer):
        #Modificar ingrediente y validación
        a = True
        for i in range(0,len(Product.objects.all())):
            if str(Ingredient.objects.all()[i]) == str(serializer.validated_data['name']):
               a = False
               print("coinciden")
        if a == True:
            serializer.save()
        
    def get_serializer_class(self):
        #Retorna clase de Serializador
        if self.action == 'retrieve':
            return serializers.IngredientDetailSerializer
        return self.serializer_class
    
    @action(methods=['get'], detail=True, url_path='some-data')
    def some(self,request,pk=None):
        return Response({
            'message': 'Some data',
            'data': request.data
        })
        

class ProductViewSet(viewsets.ModelViewSet):
    #Manejar Recetas en la base de datos
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
        
    
    def perform_create(self, serializer):
        #Crear nuevo Ingrediente
        serializer.save(user=self.request.user)
        
    def perform_update(self, serializer):
        #Modificar ingrediente y validación
        a = True
        for i in range(0,len(Product.objects.all())):
            if str(Product.objects.all()[i]) == str(serializer.validated_data['title']):
               a = False
               print("coinciden")
        if a == True:
            serializer.save()
                
        
    def get_serializer_class(self):
        #Retorna clase de Serializador
        if self.action == 'retrieve':
            return serializers.ProductDetailSerializer
        elif self.action == 'upload_image':
            return serializers.ProductImageSerializer
        return self.serializer_class
    
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        #Subir imagenes a receta
        product = self.get_object()
        serializer = self.get_serializer(
            product,
            data=request.data
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
            
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
    def _params_to_int(self,qs):
        #Convertir lista de string ID a entero
        return [int(str_id) for str_id in qs.split(',')]
    
    def get_queryset(self):
        #Retornamos los objetos para el usuario autenticado
        ingredients = self.request.query_params.get('ingredients')
        title = self.request.query_params.get('title')
        price = self.request.query_params.get('price')
        descripcion = self.request.query_params.get('descripcion')
        grupo = self.request.query_params.get('grupo')
        cantidad = self.request.query_params.get('cantidad')

        queryset = self.queryset
      
        if title:
            title_ids = title
            queryset = queryset.filter(title__icontains=title_ids)  
        if ingredients:
            ingredient_ids = self._params_to_int(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)  

        return queryset
    
    