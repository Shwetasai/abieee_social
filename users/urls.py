from users.views import (UserRegistrationView,LoginView,ForgotPasswordView,ResetPasswordView,
SuccessfullLogin)
from django.urls import path
from . import views

urlpatterns =[
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('verify/',UserRegistrationView.as_view(),name='verify'),
    path('forget-password/', ForgotPasswordView.as_view(), name='forget-password'),
    path('reset-password/<str:uidb64>/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),
    path('successfull/', SuccessfullLogin.as_view(), name='google_login'),
    path('', views.home, name='home'),

]