from django.urls import path,re_path,include
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns=[
    
    path('login',LoginView.as_view(),name='login'),
    path('signup',RegistrationView.as_view(),name='signup'),
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
