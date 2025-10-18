from django.db import models
from .eleitor import Eleitor
from .candidato import Cargo, Candidato, Eleicao


class Voto(models.Model):
    """Registra um voto anônimo para um cargo em uma eleição."""
    TIPO_VOTO_CHOICES = [
        ('VALIDO', 'Válido'),
        ('BRANCO', 'Branco'),
        ('NULO', 'Nulo'),
    ]
    eleicao = models.ForeignKey(Eleicao, on_delete=models.CASCADE, related_name='votos')
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='votos')
    candidato = models.ForeignKey(Candidato, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_voto = models.CharField(max_length=10, choices=TIPO_VOTO_CHOICES)
    data_voto = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Voto para {self.cargo.nome} em {self.eleicao.nome}"

class RegistroVotacao(models.Model):
    """Tabela para garantir que um eleitor vote apenas uma vez por eleição."""
    eleitor = models.ForeignKey(Eleitor, on_delete=models.CASCADE)
    eleicao = models.ForeignKey(Eleicao, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('eleitor', 'eleicao')

    def __str__(self):
        return f"{self.eleitor.nome} votou em {self.eleicao.nome}"