from django.contrib.auth import authenticate
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .models import CustomUserModel
from .serializers import RegisterUserSerializer, LoginUserSerializer, PublicUserSerializer
from ..utils.response_messages import ResponseMessages
from ..utils.response_type import response_item, res_error


class BaseView(generics.GenericAPIView):
    queryset = CustomUserModel
    permission_classes = (AllowAny,)


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request: Request):
        try:
            password = request.data.get('password')
            confirm_password = request.data.get('password2')
            if password != confirm_password:
                return res_error(ResponseMessages.INVALID_USER, status=status.HTTP_400_BAD_REQUEST)
            serializer = RegisterUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user = serializer.save()
            token = AccessToken.for_user(user)
            user.token = token
            user.save()
            return response_item(
                message=ResponseMessages.SUCCESS,
                item=PublicUserSerializer(user, many=False).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return res_error(str(e), status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    queryset = CustomUserModel
    serializer_class = LoginUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('email')
            password = request.data.get('password')
            user: CustomUserModel = authenticate(username=username, password=password)

            if user is not None:
                token = AccessToken.for_user(user)
                user.token = token
                user.save()
                serializer = PublicUserSerializer(user, many=False)
                return response_item(
                    message=ResponseMessages.SUCCESS,
                    item=serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response({'error': 'Invalid credentials'}, status=401)
        except Exception as e:
            print(e)
            return res_error(error=str(e), status=status.HTTP_400_BAD_REQUEST)
