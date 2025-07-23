from rest_framework import serializers
from core.models import CustomUser
from django.contrib.auth import login,authenticate

class RegistrationSerializer(serializers.ModelSerializer):
    password1=serializers.CharField(write_only=True)
    password2=serializers.CharField(write_only=True)

    class Meta:
        model=CustomUser
        fields=['user_name','email','password1','password2']

    def validate(self, attrs):
        if attrs['password1']!=attrs['password2']:
            return serializers.ValidationError('Passwords must be similar ')
        return attrs

    def create(self, validated_data):
        password=validated_data.pop('password1')
        validated_data.pop('password2')
        user=CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email=serializers.CharField(write_only=True)
    password=serializers.CharField(write_only=True)

    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')

        user=authenticate(email=email,password=password)
        if user is None:
            raise serializers.ValidationError('Please enter correct email and password ')

        attrs['user']=user
        return attrs



