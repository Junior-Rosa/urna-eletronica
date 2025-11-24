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
    candidato = models.ForeignKey(Candidato, on_delete=models.SET_NULL, null=True, blank=True, related_name='votos')
    tipo_voto = models.CharField(max_length=10, choices=TIPO_VOTO_CHOICES, editable=False)
    eleitor = models.ForeignKey(Eleitor, on_delete=models.CASCADE)
    data_voto = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('eleitor', 'eleicao','cargo')
    
    def __str__(self):
        return f"Voto para {self.cargo.nome} em {self.eleicao.nome}"

    def save(self, *args, **kwargs):
        
        if self.candidato is None:
            self.tipo_voto = 'NULO'

        if self.candidato and self.candidato.nome.upper() == 'BRANCO':
            self.tipo_voto = 'BRANCO'
        
        super().save(*args, **kwargs)