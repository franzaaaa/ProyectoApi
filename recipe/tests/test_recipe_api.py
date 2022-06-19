from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import *
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

import tempfile, os

from PIL import Image

INGREDIENTS_URL = reverse('recipe:recipe-list')

def image_upload_url(recipe_id):
    #Url de retorno para imagen de subida
    return reverse('recipe:recipe-upload_image', args=[recipe_id])

def sample_recipe(user,**params):
    #Receta de ejemplo
    defaults= {
        'title' : 'Sample',
        'time' : 10,
        'price' : 5.00
    }
    defaults.update(params)
    
    return Recipe.objects.create(user=user, **defaults)

#class UploadTest(TestCase):
#    def setUp(self):
#        self.client = APIClient()
#        self.user = get_user_model().objects.create_user('user','renaido') 
#        self.client.force_authenticate(self.user)
#        self.recipe = sample_recipe(user=self.user)
#        
#    def tearDown(self):
#        self.recipe.img.delete()
#    
#    def test_upload_image(self):
#        url = image_upload_url(self.recipe.id)
#        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
#            img = Image.new('RGB',(10,10))
#            img.save(ntf, format='JPEG')
#            ntf.seek(0)
#            res = self.client.post(url, {'image':ntf}, format='multipart')
#            
#        self.recipe.refresh_from_db()
#        self.assertEqual(res.status_code, status.HTTP_200_OK)
#        self.assertIn('image', res.data)
#        self.assertTrue(os.path.exists(self.recipe.img.path))

