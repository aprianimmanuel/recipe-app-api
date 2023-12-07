"""
Serializers for user API view
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
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

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)  # update user model object # noqa

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()  # email field
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )  # password field

    def validate(self, attrs):  # validate function to override default validate function # noqa
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),  # get request from context # noqa
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')  # if it fails, raise error # noqa
            raise serializers.ValidationError(msg, code='authorization')  # noqa

        attrs['user'] = user  # set user in attrs
        return attrs  # return attrs
