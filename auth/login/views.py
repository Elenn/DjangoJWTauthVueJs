from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .models import User
import jwt, datetime 


class RegisterView(APIView):
    def post(self, request):
        pass

class LoginView(APIView):
    def post(self, request):
        #email = request.data['email']
        password = request.data['password']
        username = request.data['username']

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response() 
        
        response.data = {
            'jwt': token
        }
        return response 

class UserView(APIView):

    def get(self, request): 
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)