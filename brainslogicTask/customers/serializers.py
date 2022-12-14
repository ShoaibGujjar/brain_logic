from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import customers
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
class UserSerializer(ModelSerializer):
    class Meta:
        model=customers
        fields=[
            "name"
        ]


class UserAuthSerializer(ModelSerializer):
    class Meta:
        model=customers
        fields=[
            'name',
            'id',
            'email'
        ]

class UserSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = customers
        fields = ['id', 'email','username', 'isAdmin','is_author']


    def get_isAdmin(self, obj):
        return obj.is_staff



class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = customers
        fields = ['id', 'name', 'email', 'isAdmin','is_author', 'token']


    

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

    def get_isAdmin(self, obj):
        return obj.is_staff