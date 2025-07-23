from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer, LoginSerializer
from django.contrib.auth import authenticate

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token)
            },
            status=status.HTTP_201_CREATED
        )

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']  # Use validated user
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token)
            },
            status=status.HTTP_200_OK
        )