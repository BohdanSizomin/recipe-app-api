from django.test import TestCase,Client
from core.models import User
from django.urls import reverse



class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(email='admin@gmail.com', password='admin123')
        self.client.force_login(self.admin_user)

        self.user = User.objects.create_user(
            email = 'test123@gmail.com',
            password='passwrd123',
            name='Test user full name',
        )
    def test_users_listed(self):
        """ Test users listed on user page"""

        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res,self.user.name)
        self.assertContains(res,self.user.email)

    def test_user_change_page(self):
        """ Test that user edit page works """
        url = reverse('admin:core_user_change',args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code,200)


    def test_create_user_page(self):
        """ Test that creates user page works"""

        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)