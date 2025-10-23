# seu_app/models.py

from django.db import models
from .eleitor import Eleitor
from django.core.exceptions import ValidationError
from django.utils import timezone


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
    data_finalizacao = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return self.nome
    
    def verificar_status(self):
        """Atualiza o status automaticamente se a data final já passou."""
        if self.data_finalizacao and self.data_finalizacao <= timezone.now() and self.status != 'FINALIZADA':
            self.status = 'FINALIZADA'
            super().save(update_fields=['status'])
            
    
    def progresso(self):

            agora = timezone.now()
            if self.data_finalizacao:
                total_dias = (self.data_finalizacao - self.data_criacao).total_seconds()
                dias_passados = (agora - self.data_criacao).total_seconds()
                progresso = (dias_passados / total_dias) * 100 if total_dias > 0 else 0
                return max(0, min(progresso, 100)) 
            else:
                return 0
    
    def save(self, *args, **kwargs):
        novo = self.pk is None
        super().save(*args, **kwargs)
        self.verificar_status()
        
        if novo:
            if self.tipo == 'PRESIDENCIAL':
                cargos = [
                    ('Presidente', 2),
                    ('Governador', 3),
                    ('Senador', 3),
                ]
            elif self.tipo == 'MUNICIPAL':
                cargos = [
                    ('Prefeito', 2),
                    ('Vereador', 4),
                ]

            for nome, digitos in cargos:
                Cargo.objects.create(eleicao=self, nome=nome, digitos=digitos)
    

class Cargo(models.Model):
    """Representa um cargo disputado em uma eleição."""
    eleicao = models.ForeignKey(Eleicao, on_delete=models.CASCADE, related_name='cargos')
    nome = models.CharField(max_length=100)
    digitos = models.PositiveSmallIntegerField(default=2, help_text="Número de dígitos do cargo, ex: 2 para prefeito, 3 para deputado")

    def __str__(self):
        return f"{self.nome} ({self.eleicao.nome})"

class Candidato(models.Model):
    """Representa um candidato concorrendo a um cargo."""
    eleitor = models.ForeignKey(Eleitor, on_delete=models.CASCADE, related_name='candidato')
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='candidatos')
    numero = models.CharField(verbose_name="Número do Candidato")
    partido = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='fotos_candidatos/', help_text="Foto do candidato")

    class Meta:
        unique_together = ('cargo', 'numero') # O número deve ser único por cargo

    def __str__(self):
        return f"{self.eleitor.nome} ({self.numero}) - {self.cargo.nome}"

    def get_votos(self):
        """Retorna o número de votos recebidos pelo candidato."""
        return self.votos.count()
    
    get_votos.short_description = "Total de Votos"
    