from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins

from core.models import Tag, Ingredient
from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):

    """
    Creating base class for Ingredient and Tag, this make it easier for the
    two classes to called the base class.
    """
    authentication_classes = (TokenAuthentication, )
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


class TagViewSet(BaseRecipeAttrViewSet):
    """
    TagViewSets for Retrieving Routers
    """
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """
    Creating IngredientViewSet
    """
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


