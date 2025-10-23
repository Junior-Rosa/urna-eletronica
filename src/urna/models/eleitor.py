
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Eleitor(models.Model):
    """Representa um eleitor."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='eleitor')
    identificador = models.CharField(max_length=50, unique=True, help_text="Ex: CPF ou Título de Eleitor")

    
    def __str__(self):
        return f"{self.user.username} ({self.identificador})"
