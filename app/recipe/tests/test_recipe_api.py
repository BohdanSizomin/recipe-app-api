from core.models import User,Recipe,Tag,Ingredient
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient


from recipe.serializers import RecipeSerializer,RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')

def sample_recipe(user, **params):
    """Create and return a sample recipe"""
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 5.00,
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


def detail_url(recipe_id):
    """ Return recipe detail URL """
    return reverse('recipe:recipe-detail',args=[recipe_id])

def sample_tag(user,name='Main Course'):
    """ Create and return simple tag """

    return Tag.objects.create(user=user,name=name)

def sample_ingredient(user,name='Cinnamon'):
    return Ingredient.objects.create(user=user,name=name)



class PublicRecipeAPITests(TestCase):
    """ Test unauthenticated recipe API access """
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """ Test unauthenticated recipe API access """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            'test@gmail.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving list of recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.data, serializer.data)
    
    def test_recipes_limited_to_user(self):
        """ Test retrieving recipes for user """
        user2 = User.objects.create_user('emailtest@gmail.com','2qewdsaqwda')
        sample_recipe(user=user2)
        sample_recipe(user=self.user)
        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """ Test viewing a recipe detail """
        recipe = sample_recipe(user = self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe,many=False)
        self.assertEqual(res.data, serializer.data)



