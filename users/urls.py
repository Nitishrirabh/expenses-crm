from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ChangePasswordView,UserRetrieveUpdateDestroyView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),
    path('user/<int:pk>', UserRetrieveUpdateDestroyView.as_view(), name='change-profile'),
]
