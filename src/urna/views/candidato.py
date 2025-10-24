from django.views.generic import TemplateView, View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from urna.models import Eleicao, Candidato, Cargo
from django.contrib import messages
from django.shortcuts import redirect
from urna.forms import CandidatarForm

class AreaCandidatoView(LoginRequiredMixin, TemplateView):
    template_name = 'area_candidato.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = self.request.user
        # Adiciona as eleições disponíveis para candidatura ao contexto
        context['eleicoes'] = Eleicao.objects.filter(status="NAO_INICIADA")
        context['candidaturas'] = set(
                Candidato.objects.filter(eleitor=user.eleitor).values_list('cargo__eleicao', flat=True)
            )
        return context

class CandidaturaView(LoginRequiredMixin, TemplateView):
    template_name = 'candidatura.html'
    
    def get_context_data(self, pk,**kwargs):
        context = super().get_context_data(**kwargs)
        cargos = Cargo.objects.filter(eleicao__pk=pk)
        context['cargos'] = cargos
        return context
    
    def get(self, request, *args, **kwargs):

        if Candidato.objects.filter(eleitor__user=request.user).exists():
            messages.error(request, 'Você já esta candidatado nesta eleição.')
            return redirect('area-candidato')
        
        
        return super().get(request, *args, **kwargs)
    
class CandidatarView(LoginRequiredMixin, CreateView):
    model = Candidato
    form_class = CandidatarForm
    template_name = 'candidatar.html'
