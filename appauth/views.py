from django.shortcuts import render
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth.hashers import make_password,check_password
# from knox.auth import TokenAuthentication
from knox.models import AuthToken
from django.contrib.auth import login,logout,authenticate
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication as TokenAuthentication
from django.views.decorators.csrf import csrf_exempt




def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegistrationView(APIView):
    permission_classes=[AllowAny,]
    serializer_class=UserSerializer

    def get(self,request):
        return Response('ok')

    def post(self,request,*args,**kwargs):
        try:
            user=User.objects.get(email=str(request.data['email']).lower())
            return Response({
                'message':'user with email already exist',
                'payload': UserSerializer(user,many=False).data,
                'success':False,
            })
        except:
            serializer=UserSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                user=serializer.instance
                

                return Response({
                    'message':'successfully signed-up',
                    'status':status.HTTP_200_OK,
                    'data':UserSerializer(user).data,
                    'success':True,
                })


class LoginView(APIView):

    permission_classes=[AllowAny,]
    authentication_classes = (BasicAuthentication,)
    serializer_class = UserSerializer


    # @csrf_exempt
    def post(self,request,*args,**kwargs):
        email=str(request.data.get('email')).strip()
        password=str(request.data.get('password')).strip()

        try:
            user=User.objects.get(email=email)

            if check_password(password,user.password):
                # Also check if user is active
                serialized_data = UserSerializer(user)
                
                token=get_tokens_for_user(user)
                # token=AuthToken.objects.create(user=user)[1]
                # login(request,user)

                return Response({
                    'token':token,
                    'user':serialized_data.data,
                    'status':status.HTTP_202_ACCEPTED,
                    'success':True,
                },status=status.HTTP_202_ACCEPTED)
            
        except ObjectDoesNotExist:
            return Response({
                'message':'user don\'t exists',
                'status':status.HTTP_404_NOT_FOUND,
                'user_exist':False,
                'success':False,
            })