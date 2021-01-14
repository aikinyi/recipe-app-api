from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user object
    """
    class Meta:
        """
        Meta class to contain all element of the serializers
        """
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5,
            }
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Updating authenticated users
        """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        # Checking if password is provided
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """
    Authentication Serializer, which will allow users to patch
    token and also validate users

    Authentication Serializer, which will allow users to patch token and also validate users
    """
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    # Function for validating users auth token
    def validate(self, attrs):
        """
        AuthToken validation for users
        """
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        # Checking if the user context is valid or not
        if not user:
            msg = _('Sorry, we are not able to authenticate you with the provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs

