from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from knox.auth import AuthToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['first_name','last_name','password','email','id','is_staff','is_superuser','is_active']
        extra_kwargs={'password':{'write_only':True},'is_staff':{'read_only':True},'is_superuser':{'read_only':True},'is_active':{'read_only':True}}


    def create(self,validated_data):
        user=User(

        email=str(validated_data['email']).lower().strip(),
        username=str(validated_data['email']).lower(),
        first_name=str(validated_data['first_name']).lower().strip(),
        last_name=str(validated_data['last_name']).lower().strip(),
        is_active=False
        )

        user.set_password(str(validated_data['password']).strip())
        user.save()

        # try:
        #     token=AuthToken.objects.get(user=user)
        # except ObjectDoesNotExist:
        #     token=AuthToken.objects.create(user=user)
        
        return user

        
        
        
