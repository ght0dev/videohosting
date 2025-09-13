from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, logout
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
class LoginView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = authenticate(
            username=serializers.validated_data['username'],
            password=serializers.validated_data['password']
        )
        
        if not user:
            return Response({'error': 'Неправильный логин или пароль'}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })
        
class LogoutView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class DeleteAccountView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
