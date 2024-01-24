"""
Views for the User API
"""
from rest_framework import generics, authentication, permissions  #  handles creating objects in the database # noqa
from rest_framework.authtoken.views import ObtainAuthToken  # obtain auth token view # noqa
from rest_framework.settings import api_settings  # settings for the project # noqa

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer  # serializer class to use for creating object # noqa


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer  # serializer class to use for creating object # noqa
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES  # renderer classes to use for creating object # noqa


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer  # serializer class to use for creating object # noqa
    authentication_classes = [authentication.TokenAuthentication]  # authentication classes to use for creating object # noqa
    permission_classes = [permissions.IsAuthenticated]  # permission classes to use for creating object # noqa

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user
