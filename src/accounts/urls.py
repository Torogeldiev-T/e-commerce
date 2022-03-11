from os import name
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('login', views.user_login, name='user_login'),
]
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
