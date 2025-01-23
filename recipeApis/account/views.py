from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status ,exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer
import jwt,datetime

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None :
            raise exceptions.AuthenticationFailed('User does not exist')
        print(user)
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Incorrect Password')

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode( payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key = 'jwt', value = token ,httponly=True)

        response.data = {
            'jwt': token,
            'status': status.HTTP_200_OK
        }

        return response

class UserView(APIView):
    def get(self, request):
        # Extract the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            raise exceptions.AuthenticationFailed('Authorization header with Bearer token is missing')

        # Remove the "Bearer " prefix to get the token
        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

        user = User.objects.filter(id=payload['id']).first()
        if not user:
            raise exceptions.AuthenticationFailed('User not found')

        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "Successfully logged out"
        }
        return response