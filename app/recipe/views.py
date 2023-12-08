"""
Views for the recipe app
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for recipe objects.
    """
    authentication_classes = [TokenAuthentication]  # use TokenAuthentication. Default is SessionAuthentication. # noqa
    permission_classes = [IsAuthenticated]  # use IsAuthenticated. Default is AllowAny. # noqa
    queryset = Recipe.objects.all()  # get all recipes
    serializer_class = serializers.RecipeSerializer  # use RecipeSerializer

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
