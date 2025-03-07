from .models import Profile
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email' , 'url']

class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'password')
        extra_kwargs={'password':{
            'write_only' : True
        }}

    def create(self, validated_data):
        
        return User.objects.create_user(**validated_data)
    
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {
            'profile': {'write_only': True},
        }