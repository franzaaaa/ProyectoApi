from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from yaml import serialize

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')

class PublicIngredientsApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
    def test_login_required(self):
        res = self.client.get(INGREDIENTS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
class PrivateIngredientsApiTest(TestCase):
    def setUp(self):
       self.client = APIClient()
       self.user = get_user_model().objects.create_user(
           'test@test.com'
           'test123'
       )
       self.client.force_authenticate(self.user)
       
    def test_retrieve_ingredients(self):
        #Probamos obtención de ingredientes
        Ingredient.objects.create(user=self.user, name='Meat')
        Ingredient.objects.create(user=self.user, name='Fruit')
        
        res = self.client.get(INGREDIENTS_URL)
        
        ingredients = Ingredient.objects.order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        
    def test_create_ingredient(self):
        #Probamos creación de un nuevo ingrediente
        payload = {
            'name' : 'Simple'
        }
        self.client.post(INGREDIENTS_URL, payload)
        
        exists = Ingredient.objects.filter(
            user=self.user, 
            name=payload['name']
        ).exists()
        self.assertTrue(exists)
        
    def test_create_invalid(self):
        #Probamos creación con payload invalido
        payload = {
            'name' : ''
        }
        res = self.client.post(INGREDIENTS_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        