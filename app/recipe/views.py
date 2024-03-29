"""
Views for the recipe app
"""
from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for recipe objects.
    """
    authentication_classes = [TokenAuthentication]  # use TokenAuthentication. Default is SessionAuthentication. # noqa
    permission_classes = [IsAuthenticated]  # use IsAuthenticated. Default is AllowAny. # noqa
    queryset = Recipe.objects.all()  # get all recipes
    serializer_class = serializers.RecipeDetailSerializer  # use RecipeDetailSerializer # noqa

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')  # filter the queryset # noqa

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':  # if the action is list
            return serializers.RecipeSerializer  # use RecipeSerializer

        return self.serializer_class  # otherwise use the default serializer

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)


class TagViewSet(mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """
    ViewSet for tags.
    """
    authentication_classes = [TokenAuthentication]  # use TokenAuthentication. Default is SessionAuthentication. # noqa
    permission_classes = [IsAuthenticated]  # use IsAuthenticated. Default is AllowAny. # noqa
    queryset = Tag.objects.all()  # get all recipes
    serializer_class = serializers.TagSerializer  # use TagSerializer # noqa

    def get_queryset(self):
        """Retrieve tags for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')  # filter the queryset # noqa


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Manage ingredients in the database."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')
