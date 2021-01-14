from rest_framework import generics, permissions, authentication
from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(generics.CreateAPIView):
    """
    Creating user view
    """
    serializer_class = UserSerializer


class CreateAuthTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Creating endpoint for managing user
    """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        """
        Returning user data
        """
        return self.request.user

