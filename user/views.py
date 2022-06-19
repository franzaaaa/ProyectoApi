from distutils.log import error
from django.http import JsonResponse
from html5lib import serialize
from rest_framework.response import Response
from rest_framework import generics, authentication, permissions, authtoken
from core.models import User, Mods
from user.serializers import PasswordSerializer, UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from django.urls import reverse

from rest_framework.settings import api_settings
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from .renderers import UserRenderer

class CreateUserView(generics.CreateAPIView):
    #Crear nuevo usuario
    serializer_class = UserSerializer
    renderer_classes = (UserRenderer,)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['email']

        current_site = get_current_site(request)
        absurl = current_site
        email_body = 'Hi '+user+' we want you to verify your account\n '+'Hit this link '+'http://'+str(absurl)+'/api/user/token'
        data = {
            'body' : email_body,
            'email' : user,
            'subject' : 'Verify email'
        }
        #user = User(email=serializer.validated_data['email'], password=serializer.validated_data['password'], name=serializer.validated_data['name'], is_active=0)
        user = get_user_model().objects.create_user(**serializer.validated_data)
        user.save()
        #Envio de email
        Util.send_email(data)
        return Response({'message': 'Usuario creado', 'user':user.email})
          
class CreateTokenView(ObtainAuthToken):
    #Creacion de nuevo auth token para el usuario
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
        
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        u = User.objects.get(email = serializer.validated_data['user'])
        u.is_validated=True
        u.save()
        
        user = serializer.validated_data['user']
        
        token, created = Token.objects.get_or_create(user=user)
       
        return Response({
           'token': token.key,
           'user_id': user.pk,
           'email': user.email
       })
            
class ManageUserView(generics.RetrieveUpdateAPIView):
    #Manejar usuario autenticado
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        #Obtener y retornar usuario autenticado      
        return self.request.user
        #return User.objects.all()
          
class UserApiView2(APIView):
    
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, format = None):
        usernames = [user.email for user in User.objects.all()]
        print(self.request.auth)
        return Response(usernames)
    
class UserApiView(viewsets.ModelViewSet):
    
    #authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.filter(is_validated = True)
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=True, url_path='change-password')
    def change_password(self,request,pk=None):
        user = self.get_object()
        password_serializer = PasswordSerializer(data=request.data)
        if password_serializer.is_valid():
            Mods.objects.create(user=user, date="10-11-2002")
            user.set_password(password_serializer.validated_data['password'])
            user.save()
            return Response({'message':'Contraseña actualizada'})
        return Response(
            {
            'message':'Contraseña no actualizada',
            'errors': password_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        #Modificar usuario y validación
        a = True
        for i in range(0,len(Product.objects.all())):
            if str(User.objects.all()[i]) == str(serializer.validated_data['email']):
               a = False
               print("coinciden")
        if a == True:
            serializer.save()

    