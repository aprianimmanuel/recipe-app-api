"""
Views for the User API
"""
from rest_framework import generics  #  handles creating objects in the database # noqa
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer  # serializer class to use for creating object # noqa