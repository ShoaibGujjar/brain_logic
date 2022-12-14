from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
# from django.contrib.auth.models import User
from .models import customers
from datetime import datetime
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer, UserSerializerWithToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.customers).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUser(request):
    data = request.data
    alreadyExists = customers.objects.filter(email=data['email']).exists()
    if alreadyExists:
        content = {'detail': 'already exist'}
        return Response(content) 
    else:
        try:
            customers = customers.objects.create(
                username=data['username'],
                email=data['email'],
                password=make_password(data['password']),
            )
            serializer = UserSerializerWithToken(customers, many=False)
            return Response(serializer.data)
        except:
            message = {'detail': 'Detail was not correct'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    customers = request.customers
    serializer = UserSerializerWithToken(customers, many=False)

    data = request.data
    customers.email= data['email']
    customers.username=data['username']
    if data['password'] != '':
        customers.password = make_password(data['password'])

    customers.save()

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.customers
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = customers.objects.all()
    serializer = UserSerializer(users, many=True)

 
    # user can only update once every 10 minutes : 10 set in model
    last_login = customers.objects.filter(customers=request.customers).latest('id')
    current_time = datetime.now().replace(tzinfo=None)   
    next_allowed_update = last_login.last_login.replace(tzinfo=None)

    remaining = str(next_allowed_update - current_time).split(':')
    minutes_remaining = int(remaining[1].lstrip("0")) + 1
    if current_time > next_allowed_update:
        message='can get user'
        return Response(detail={message})
    else:
        message='can not get user'
        return Response(detail={message})
        
    return Response(serializer.data)