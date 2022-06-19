import email
from unicodedata import name
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTest(TestCase):
    #Testear API pública del usuario
    def setUp(self):
        self.client = APIClient()
        
    #def test_create_valid_user_success(self):
    #    #Probar crear usuario con payload exitoso
    #    payload = {
    #        'email' : 'test@gmail.com',
    #        'password' : 'root',
    #        'name' : 'test name'
    #    }
    #    
    #    res = self.client.post(CREATE_USER_URL, payload)
    #    
    #    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #    user = get_user_model().objects.get(**res.data)
    #    self.assertTrue(user.check_password(payload['password']))
    #    self.assertNotIn('password',res.data)
    #    
    def test_user_exists(self):
        #Prueba creación usuario que ya existe
        payload = {
            'email' : 'test@gmail.com',
            'password' : 'root',
            'name' : 'test'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_password_short(self):
        #Probar contraseña demasiado corta
        payload = {
            'email' : 'test@gmail.com',
            'password' : 'ro', 
            'name' : 'test'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)
        
    def test_create_token(self):
        #Probar que el token se creó para el usuario
        payload = {
            'email' : 'test@gmail.com',
            'password' : 'root', 
            'name' : 'test'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_create_token_invalid_credentials(self):
        #Probar que el token no es creado con creedenciales invalidas
        create_user(email='test@gmail.com', password='root')
        payload= {
            'email' : 'test@gmail.com',
            'password' : '123'
        }
        res = self.client.post(TOKEN_URL, payload)
        
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_token_no_user(self):
        #Probamos que no se cree el token si no existe usuario
        payload = {
            'email' : 'test@gmail.com',
            'password' : 'root'
        }
        res = self.client.post(TOKEN_URL, payload)
        
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_token_no_field(self):
        #Probamos que email y psw sean requeridos
        res = self.client.post(TOKEN_URL, {'email' : 'one', 'password' : ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        

    def test_retrieve_user_unauthorized(self):
        #Probamos que la autenticación sea requerida para los usuarios
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
class PrivateUserApiTest(TestCase):
    #Probar el API privado del usuario
    
    def setUp(self):
        self.user = create_user(
            email = 'test@test.com',
            password = 'test',
            name = 'test'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
    def test_retrieve_profile_success(self):
        #Probamos obtención de perfil para usuario logeado
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name' : self.user.name,
            'email' : self.user.email
        })
        
    def test_post_me_not_allowed(self):
        #Probamos que el post no sea permitido
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_update_user_profile(self):
        #Probamos que el usuario está siendo actualizado si está autentificado
        payload = {
            'name' : 'newtest',
            'password' : 'newtest'
        }
        
        res = self.client.patch(ME_URL, payload)
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)