# seu_app/models.py

from django.db import models


class Eleicao(models.Model):
    """Representa uma eleição."""
    TIPO_ELEICAO_CHOICES = [
        ('PRESIDENCIAL', 'Presidente, Governador e Senador'),
        ('MUNICIPAL', 'Prefeito e Vereador'),
    ]
    
    STATUS_CHOICES = [
        ('NAO_INICIADA', 'Não Iniciada'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('FINALIZADA', 'Finalizada'),
    ]

    nome = models.CharField(max_length=200, verbose_name="Nome da Eleição")
    tipo = models.CharField(max_length=20, choices=TIPO_ELEICAO_CHOICES, verbose_name="Tipo de Eleição")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NAO_INICIADA', verbose_name="Status")
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Cargo(models.Model):
    """Representa um cargo disputado em uma eleição."""
    eleicao = models.ForeignKey(Eleicao, on_delete=models.CASCADE, related_name='cargos')
    nome = models.CharField(max_length=100)
    digitos = models.PositiveSmallIntegerField(default=2)

    def __str__(self):
        return f"{self.nome} ({self.eleicao.nome})"

class Candidato(models.Model):
    """Representa um candidato concorrendo a um cargo."""
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='candidatos')
    nome = models.CharField(max_length=200)
    numero = models.PositiveIntegerField(verbose_name="Número do Candidato")
    partido = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='fotos_candidatos/', blank=True, null=True)

    class Meta:
        unique_together = ('cargo', 'numero') # O número deve ser único por cargo

    def __str__(self):
        return f"{self.nome} ({self.numero}) - {self.cargo.nome}"


