from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth import password_validation, authenticate
from drf_extra_fields.fields import Base64ImageField
from the_big_username_blacklist import validate as validate_username

from .models import User


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)

    class Meta:
        fields = ['username', 'password']

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            attrs['user'] = user
        else:
            raise ValidationError('Wrong username or password')
        return attrs


class UserMeSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    profile_photo = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "token",
            "password",
            "profile_photo",
            "bio",
            "first_name",
            "last_name",
            "remaining_modifier",
            "verified",
        ]
        extra_kwargs = {'password': {'write_only': True}, 'remaining_modifier': {'read_only': True}, "verified": {"read_only": True}}

    def create(self, validated_data):
        username = validated_data.get("username")
        if not validate_username(username):
            raise ValidationError("Invalid username")
        password = validated_data.get('password')
        try:
            password_validation.validate_password(password)
        except:
            raise ValidationError('Password is not valid')
        user = User.objects.create_user(**validated_data)
        return user

    def get_token(self, user):
        token = Token.objects.get(user=user)
        return token.key


class UserDetailSerializer(serializers.ModelSerializer):
    profile_photo = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "bio",
            "profile_photo"
        ]


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "profile_photo",
            "skill_point",
        ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetPasswordCreationSerializer(serializers.Serializer):
    user_identifier = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    key = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
