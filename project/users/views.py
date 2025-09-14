from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, logout
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

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


class ProfileView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
    
class ProfileUpdateView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateProfileSerializer
    
    def get_object(self):
        return self.request.user
    
class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.send_password_reset_email()
        
        return Response(
            {"detail": "Письмо со ссылкой на сброс пароля отправлено"},
            status=status.HTTP_200_OK
        )

    
class ResetPasswordConfirmView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordConfirmSerializer
    
    def get_serializer(self, *args, **kwargs):
        
        data = kwargs.get('data', self.request.data).copy()
        data['uid'] = self.kwargs.get('uidb64')
        data['token'] = self.kwargs.get('token')
        kwargs['data'] = data
        return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Пароль успешно изменен"}, status=200)
