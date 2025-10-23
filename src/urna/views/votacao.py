from django.views import View
from django.views.generic import ListView
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Eleicao, Voto
import csv
from django.http import HttpResponse


class IndexView(LoginRequiredMixin, ListView):
    
    model = Eleicao
    template_name = 'index.html'
    context_object_name = 'eleicoes'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context['eleicoes_andamento'] = context['eleicoes'].filter(status='EM_ANDAMENTO')
        context['eleicoes_finalizadas'] = context['eleicoes'].filter(status='FINALIZADA')
        context['votacoes_usuario'] = set(
            Voto.objects.filter(eleitor=user.eleitor).values_list('eleicao_id', flat=True)
        )
        return context
    

class EleicaoRelatorioCSV(LoginRequiredMixin, View):
    """Gera um relatório CSV com os votos de uma eleição."""
    def get(self, request, pk):
        eleicao = Eleicao.objects.get(pk=pk)
        votos = eleicao.votos.all()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="relatorio_{eleicao.nome}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Eleitor', 'Candidato', 'Data do Voto'])

        for voto in votos:
            writer.writerow([voto.eleitor, voto.candidato, voto.data_voto.strftime('%d/%m/%Y %H:%M')])

        return response