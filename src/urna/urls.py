from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# app_name = 'urna'

urlpatterns = [
    # Admin URLs
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('', views.IndexView.as_view(), name='index'),
    path('logout/', auth_views.LogoutView.as_view(http_method_names=['get', 'post']), name='logout'),
    
]