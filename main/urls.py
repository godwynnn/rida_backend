from django.urls import path,re_path,include
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns=[
    path('data',RideCostDataView.as_view(),name='ride_cost_data')
]
