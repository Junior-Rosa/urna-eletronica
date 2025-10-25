from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# app_name = 'urna'

urlpatterns = [
    # Admin URLs
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(http_method_names=['get', 'post']), name='logout'),
    path('register/', views.register, name='registro'),
    
    
    path('', views.IndexView.as_view(), name='index'),
    path('candidato/', views.AreaCandidatoView.as_view(), name='area-candidato'),
    path('candidatura/<int:pk>/', views.CandidaturaView.as_view(), name='candidatura'),
    path('candidatar/<int:pk>', views.CandidatarCreateView.as_view(), name='candidatar'),
    path('candidatos/<int:pk>', views.CandidatosListView.as_view(), name='candidatos'),
    path('relatorio/<int:pk>/', views.EleicaoRelatorioCSV.as_view(), name='relatorio-csv'),
    
]