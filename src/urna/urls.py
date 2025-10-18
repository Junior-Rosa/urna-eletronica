from django.urls import path
from . import views
from django.contrib.auth import login 
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Admin URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
]