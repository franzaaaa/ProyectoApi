import pprint
from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from yaml import serialize

from core.models import Recipe, Tag
from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')

class PublicTagsApiTest(TestCase):
    #Prueba de API tags disponibles publicamente
    def setUp(self):
        self.client = APIClient()
        
    #def test_login_required(self):
    #    #Probamos que el login sea requerido
    #    res = self.client.get(TAGS_URL)
    #    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
class PrivateTagsApiTest(TestCase):
    #Prueba de API tags disponibles publicamente
    def setUp(self):
        self.user = get_user_model().objects.create_user(
           'prueba3@prueba3.com',
           'prueba3'  
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        
    def test_retrieve_tags(self):
        #Probamos obtención de tags
        Tag.objects.create(user=self.user, name='Meat')
        Tag.objects.create(user=self.user, name='Fruit')
        
        res = self.client.get(TAGS_URL)
        
        tags = Tag.objects.order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        
    def test_tags_limited_to_user(self):
        #Probamos que se retornan los tags del usuario
        user2 = get_user_model().objects.create_user(
           'prueba4@prueba3.com',
           'prueba4'  
        )
        Tag.objects.create(user=user2, name='Vegetables')
        tag = Tag.objects.create(user=self.user, name='123')
        
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'], tag.name)
        
    def test_create_tag(self):
        #Probamos creación de un nuevo tag
        payload = {
            'name' : 'Simple'
        }
        self.client.post(TAGS_URL, payload)
        
        exists = Tag.objects.filter(
            user=self.user, 
            name=payload['name']
        ).exists()
        self.assertTrue(exists)
        
    def test_create_invalid(self):
        #Probamos creación con payload invalido
        payload = {
            'name' : ''
        }
        res = self.client.post(TAGS_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_retrieve_tags_recipes(self):
        #Filtrado con tags
        tag1 = Tag.objects.create(user=self.user, name='Breakfast')
        tag2 = Tag.objects.create(user=self.user, name='Prueba')
        recipe = Recipe.objects.create(
            title='Una receta',
            time=10,
            price=1.00,
            user=self.user
        )
        recipe.tags.add(tag1)
        res = self.client.get(TAGS_URL, {'assigned_only':1})
        
        serializer1 = TagSerializer(tag2)
        #self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer1.data, res.data)