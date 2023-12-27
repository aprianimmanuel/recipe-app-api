"""
Serializers for recipe app
"""
from rest_framework import serializers

from core.models import (
    Recipe,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects."""

    class Meta:
        """Meta class for serializer."""
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects."""
    tags = TagSerializer(many=True, required=False)

    class Meta:
        """Meta class for serializer."""
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a recipe."""
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

        return recipe


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail objects."""

    class Meta(RecipeSerializer.Meta):
        """Meta class for serializer."""
        fields = RecipeSerializer.Meta.fields + ['description']
