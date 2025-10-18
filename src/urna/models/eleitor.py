
from django.db import models


class Eleitor(models.Model):
    """Representa um eleitor."""
    identificador = models.CharField(max_length=50, unique=True, help_text="Ex: CPF ou Título de Eleitor")
    nome = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.nome} ({self.identificador})"
