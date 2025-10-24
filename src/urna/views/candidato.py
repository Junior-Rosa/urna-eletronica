from django.views.generic import TemplateView, View, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from urna.models import Eleicao, Candidato, Cargo, Eleitor
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
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
        eleitor = get_object_or_404(Eleitor, user=request.user)
        eleicao_id = self.kwargs.get('pk')

        # Verifica se já há candidato para esta eleição
        if Candidato.objects.filter(eleitor=eleitor, cargo__eleicao__pk=eleicao_id).exists():
            messages.error(request, 'Você já está candidatado nesta eleição.')
            return redirect('area-candidato')

        # Caso não esteja candidato, renderiza a página normalmente
        return super().get(request, *args, **kwargs)
    
class CandidatarCreateView(LoginRequiredMixin, CreateView):
    model = Candidato
    form_class = CandidatarForm
    template_name = 'candidatar.html'


    def dispatch(self, request, *args, **kwargs):
        """
        Garante que o cargo existe e impede candidaturas duplicadas.
        """
        
        self.cargo = get_object_or_404(Cargo, pk=self.kwargs['pk'])
        if Candidato.objects.filter(eleitor=request.user.eleitor, cargo=self.cargo).exists():
            messages.warning(request, "Você já é candidato para este cargo.")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    
    def get_form(self, form_class:CandidatarForm=None):
        form = super().get_form(form_class)
        eleitor = get_object_or_404(Eleitor, user=self.request.user)
        form.instance.eleitor = eleitor
        form.instance.cargo = self.cargo
        return form
    
    def form_valid(self, form:CandidatarForm):
        """
        Define automaticamente o usuário e o cargo antes de salvar.
        """
        # eleitor = get_object_or_404(Eleitor, user=self.request.user)
        # form.instance.eleitor = eleitor
        # form.instance.cargo = self.cargo
        messages.success(self.request, "Candidatura realizada com sucesso!")
        # print(form.instance)
        return super().form_valid(form)
    
    def get_success_url(self):
        """
        Redireciona de volta para a página da eleição.
        """
        return reverse('area-candidato')
    
    def get_context_data(self, **kwargs):
        """
        Adiciona o cargo e a eleição ao contexto do template.
        """
        context = super().get_context_data(**kwargs)
        context['cargo'] = self.cargo
        context['eleicao'] = self.cargo.eleicao
        return context
    
class CandidatosListView(LoginRequiredMixin, ListView):
    model = Candidato
    template_name = 'candidatos.html'
    context_object_name = 'candidatos'
    
    def get_queryset(self):
        eleicao = get_object_or_404(Eleicao, pk=self.kwargs.get('pk'))
        return Candidato.objects.filter(cargo__eleicao=eleicao)