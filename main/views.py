from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication as TokenAuthentication
from django.views.decorators.csrf import csrf_exempt
import requests


GOOGLE_API_URL='https://maps.googleapis.com/maps/api'

class RideCostDataView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        data=request.data
        if None not in [data['origin'],data['destination']]:
            url=f"""{GOOGLE_API_URL}/distancematrix/json?origins={data['origin']['lat']},
            {data['origin']['lng']}&destinations={data['destination']['lat']},
            {data['destination']['lng']}&mode=driving&language=en-EN&sensor=false&key={settings.GOOGLE_API_KEY}"""

            
            res=requests.get(url=url)
            response=res.json()
            distance=response['rows'][0]['elements'][0]['distance']['text']
            prices=[
                {
                    'title':'Economy',
                    'amount':int(500*float(str(distance).split(' ')[0])),
                    'distance':str(distance),
                    'time':response['rows'][0]['elements'][0]['duration']['text']
                },
                {
                    'title':'Standard',
                    'amount':int(590*float(str(distance).split(' ')[0])),
                    'distance':str(distance),
                    'time':response['rows'][0]['elements'][0]['duration']['text']
                },
                {
                    'title':'Premium',
                    'amount':int(800*float(str(distance).split(' ')[0])),
                    'distance':str(distance),
                    'time':response['rows'][0]['elements'][0]['duration']['text']
                }
                ]
            # print(prices)

            return Response({
                'data':prices,
                'success':True
            })
        else:
            # print(False)
            return Response({
                'data':{},
                'success':False
            })