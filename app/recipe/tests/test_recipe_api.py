"""
Tests for recipe API
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
)


RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Create and Return a recipe detail URL"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe(user, **params):
    """Helper function to create a recipe."""
    defaults = {
        'title': 'Sample recipe title',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'http://example.com/recipe.pdf',
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


class PublicRecipeAPITests(TestCase):
    """Test unauthenticated recipe API access."""

    def setUp(self):
        """Setup the test client."""
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required."""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """Test authenticated recipe API access."""

    def setUp(self):
        """Setup the test client."""
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_list_limited_to_user(self):
        """Test retrieving recipes for user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_recipe(user=other_user)  # create a recipe for the other user
        create_recipe(user=self.user)  # create a recipe for the authenticated user # noqa

        res = self.client.get(RECIPES_URL)  # get the recipes

        recipes = Recipe.objects.filter(user=self.user)  # filter the recipes
        serializer = RecipeSerializer(recipes, many=True)  # serialize the recipes # noqa
        self.assertEqual(res.status_code, status.HTTP_200_OK)  # assert the status code # noqa
        self.assertEqual(res.data, serializer.data)  # assert the data

    def test_get_recipe_detail(self):
        """Test retrieving a recipe detail."""
        recipe = create_recipe(user=self.user)  # create a recipe

        url = detail_url(recipe.id)  # get the recipe detail url
        res = self.client.get(url)  # get the recipe detail

        serializer = RecipeDetailSerializer(recipe)  # serialize the recipe
        self.assertEqual(res.data, serializer.data)  # assert the data