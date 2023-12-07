"""
Serializers for user API view
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):  # base class for defining serializer # noqa
    """Serializer for user object"""

    class Meta:  # class to configure serializer
        model = get_user_model()  # get user model from Django
        fields = ('email', 'password', 'name')  # fields to include in serializer # noqa
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}  # extra keyword args to configure fields # noqa

    def create(self, validated_data):  # create function to override default create function # noqa
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)  # create user model object # noqa