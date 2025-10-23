from django.views import View
from django.views.generic import ListView
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Eleicao

class IndexView(LoginRequiredMixin, ListView):
    
    model = Eleicao
    template_name = 'index.html'
    context_object_name = 'eleicoes'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agora = timezone.now()

        for eleicao in context['eleicoes']:
            if eleicao.data_finalizacao:
                total_dias = (eleicao.data_finalizacao - eleicao.data_criacao).total_seconds()
                dias_passados = (agora - eleicao.data_criacao).total_seconds()
                progresso = (dias_passados / total_dias) * 100 if total_dias > 0 else 0
                eleicao.progresso = max(0, min(progresso, 100)) 
            else:
                eleicao.progresso = 0

        return context