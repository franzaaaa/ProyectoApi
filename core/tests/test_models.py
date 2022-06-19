from unicodedata import name
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from unittest.mock import patch

        
        
def sample_user(email='prueba2@prueba2.com', password='prueba2'):
    return get_user_model().objects.create_user(email,password)




class ModelTest(TestCase):
    def test_create_user(self):
        #Probar creación de usuario con email correctamente
        email = 'xfranza2001@gmail.com'
        password = '123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))
        
    def test_new_user_normalized(self):
        #Testea email para nuevo usuario normalizado
        email = 'xfranza2001@GMAIL.com'
        user = get_user_model().objects.create_user(
            email, 
            '123'      
        )
        self.assertEqual(user.email, email.lower())
        
    def test_new_user_invald(self):
        #Nuevo usuario email invalido
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '123')
            
    def test_create_superuser(self):
        #Probar superusuario creado
        email = 'xfranza@gmail.com'
        password = '123'
        user = get_user_model().objects.create_superuser(
            email = email,
            password = password
        )
        self.assertEqual(user.email,email)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        
    def test_tag_str(self):
       #Probar representación en texto del tag
       tag = models.Tag.objects.create(
           user = sample_user(),
           name='Meat'
       )
       
       self.assertEqual(str(tag), tag.name)
       
    def test_ingredient_str(self):
        #Probar representación en texto del ingrediente
        ingredient = models.Ingredient.objects.create(
            user = sample_user(),
            name='Banana'
        )
        
        self.assertEqual(str(ingredient), ingredient.name)
        
    @patch('uuid.uuid4')   
    def test_recipe_file_name(self,mock_uuid):
        #Probar que imagen se guarda en luagr correcto
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None,' myimage.jpg')
        
        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)