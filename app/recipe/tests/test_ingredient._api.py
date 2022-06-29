from core.models import User
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')

class PublicIngredient(TestCase):
    """ Test the publicly available ingredients API """
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientAPITests(TestCase):
    """ Test Ingredient can be retrievied by authorized user """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email = 'test@gmail.com',
            password = 'pass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """ Test retrieving a list of ingredients """
        Ingredient.objects.create(
            user = self.user,
            name='Kale',
        )
        Ingredient.objects.create(
            user = self.user,
            name='Salt',
        )

        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients,many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """ Test that only ingerdients for the authenticated user are returned """
        user2 = User.objects.create_user(
            'testuser@gmail.com',
            'password12321321'
        )
        Ingredient.objects.create(user=user2,name='Vinegar')
        Ingredient.objects.create(user=self.user,name='Tumeric')
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
