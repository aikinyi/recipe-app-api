from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins

from core.models import Tag
from recipe import serializers


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """
    TagViewSets for Retrieving Routers
    """
    authentication_classes = (TokenAuthentication, )
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """
        Getting filtering  base on user that authenticated
        """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """
        Creating new tag
        """
        serializer.save(user=self.request.user)
