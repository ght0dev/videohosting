from rest_framework import serializers
from .models import User
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

token_generator = PasswordResetTokenGenerator()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'subscriptions']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Пароли не совпадают'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'subscriptions']
        
class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'email', 'username']
        
class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError({'email': 'Пользователь с таким email не найден'})
        return value

    def send_password_reset_email(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        send_mail(
            subject='Запрос на смену пароля!',
            message=f"Ссылка для сброса пароля: {reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=f"""
                <p>На ваш email отправлен запрос на смену пароля.</p>
                <p><a href="{reset_url}">Сбросить пароль</a></p>
                <p>Если вы не запрашивали смену пароля — проигнорируйте письмо.</p>
            """
        )

        
class ResetPasswordConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, attrs):
        try:
            uid = urlsafe_base64_decode(attrs['uid']).decode()
            self.user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            raise serializers.ValidationError({'uid': 'Неверный UID'})

        if not token_generator.check_token(self.user, attrs['token']):
            raise serializers.ValidationError({'token': 'Неверный или просроченный токен'})
        
        return attrs

    def save(self):
        new_password = self.validated_data['new_password']
        self.user.set_password(new_password)
        self.user.save()
        return self.user
    