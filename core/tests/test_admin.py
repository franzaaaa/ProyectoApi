from audioop import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'xfranza2001@gmail.com',
            password = 'root'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'test@gmail.com',
            password = 'root',
            name = 'test'
        )
        
    def test_users_listed(self):
        'Testear que los usuarios fueron listados en la página de usuario'
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
        
    def test_user_change_page(self):
        #Probamos que la página editada por el usuario funciona
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, 200)
        
    def test_create_user_page(self):
        #Testear que la página de Crear usuario funciona
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, 200)