from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import VotoForm
from ..models import Eleicao, Voto, Cargo
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
        if hasattr(user, 'eleitor'):
            context['votacoes_usuario'] = set(
                Voto.objects.filter(eleitor=user.eleitor).values_list('eleicao_id', flat=True)
            )

        return context
    
    def get_queryset(self):
        
        qs = super().get_queryset()
        for eleicao in qs:
            eleicao.verificar_status()
        return qs

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

class CargosView(LoginRequiredMixin, CreateView):
    model = Voto
    template_name = 'cargos.html'
    form_class = VotoForm
    success_url = reverse_lazy('success-page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['cargos'] = Cargo.objects.filter(eleicao__pk=pk)
        context['eleicao'] = Eleicao.objects.get(pk=pk)
        return context

    def get_success_url(self):
        return reverse('index')