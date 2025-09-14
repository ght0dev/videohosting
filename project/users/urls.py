from django.urls import path
from .views import *

urlpatterns = [
    
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/', DeleteAccountView.as_view(), name='delete'),
    
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile-update/', ProfileUpdateView.as_view(), name='profile-update'),
    
    path('request-password-reset/', RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='password-reset'),

]
