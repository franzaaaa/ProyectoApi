from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers
from yaml import serialize

class UserSerializer(serializers.ModelSerializer):
    #Serializador para modelo Users
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name', 'telefono', 'direccion')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        
    def create(self, validated_data):
        #Crear nuevo usuario con la clave encriptada y lo retornamos
        return get_user_model().objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        #Actualiza al usuario, configura el password y lo retorna
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user
    
#class AuthTokenSerializer(serializers.Serializer):
#    #Serializador para objeto de autentificación de usuario
#    email = serializers.CharField()
#    password = serializers.CharField(
#        style = {'input_type': 'password'},
#        trim_whitespace = False
#    )
#    
#    def validate(self, attrs):
#        #Validar y autenticar usuarios
#        email = attrs.get('email')
#        password = attrs.get('password')
#        
#        user = authenticate(
#            request = self.context.get('request'),
#            username = email,
#            password = password
#        )
#        if not user:
#            msg = 'Unable to authenticate with provided credentials'
#            raise serializers.ValidationError(msg, code='authorization')
#        
#        attrs['user'] = user
#        return attrs


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, min_length=4, write_only=True)
    password2 = serializers.CharField(max_length=128, min_length=4, write_only=True)
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Contraseñas deben ser iguales")
        return data