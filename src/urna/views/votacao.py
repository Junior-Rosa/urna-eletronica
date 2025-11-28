from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import VotoForm
from ..models import Eleicao, Voto, Cargo, Candidato
import csv
from django.http import HttpResponse, JsonResponse


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

class CargosView(LoginRequiredMixin, TemplateView):
    model = Voto
    template_name = 'cargos.html'
    success_url = reverse_lazy('index')
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['cargos'] = Cargo.objects.filter(eleicao__pk=pk)
        context['eleicao'] = Eleicao.objects.get(pk=pk)
        return context

    def get_success_url(self):
        return reverse('index')

class VotoCreateView(LoginRequiredMixin, CreateView):
    model = Voto
    form_class = VotoForm
    template_name = 'votar.html'
    success_url = reverse_lazy('index')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if self.request.session.get('eleicao_atual') != self.kwargs['pk'] or self.request.session.get('eleicao_atual') is None:
            self.request.session['eleicao_atual'] = self.kwargs['pk']
            self.request.session['cargos_votados'] = 0
            self.request.session['votos_pendentes'] = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['eleicao'] = Eleicao.objects.get(pk=pk)
        cargos = Cargo.objects.filter(eleicao__pk=pk).order_by('id')
        count_cargos = cargos.count()

        cargos_votados = self.request.session.get('cargos_votados', 0)

        if cargos_votados >= count_cargos:
            context['cargo'] = None
            context['voting_complete'] = True
        else:
            context['cargo'] = cargos[cargos_votados]
            context['voting_complete'] = False

        context['total_cargos'] = count_cargos

        return context

    def form_valid(self, form):
        action = self.request.POST.get('action', 'votar')

        if action == 'branco':
            candidato_id = None
            tipo_voto = 'BRANCO'

            messages.info(self.request, "Voto em branco registrado!")
        else:
            numero_candidato = self.request.POST.get('numero_candidato', '').strip()
            cargo = form.cleaned_data['cargo']

            if numero_candidato:
                try:
                    candidato = Candidato.objects.get(cargo=cargo, numero=numero_candidato)
                    candidato_id = candidato.id
                    tipo_voto = 'VALIDO'
                    messages.success(self.request, f"Voto registrado para o candidato {numero_candidato}!")
                except Candidato.DoesNotExist:
                    candidato_id = None
                    tipo_voto = 'NULO'
                    messages.warning(self.request, f"Número {numero_candidato} inválido. Voto nulo registrado!")
            else:
                candidato_id = None
                tipo_voto = 'NULO'
                messages.warning(self.request, "Nenhum número digitado. Voto nulo registrado!")

        voto_data = {
            'eleitor_id': form.cleaned_data['eleitor'].id,
            'cargo_id': form.cleaned_data['cargo'].id,
            'candidato_id': candidato_id,
            'eleicao_id': form.cleaned_data['eleicao'].id,
            'tipo_voto': tipo_voto,
        }

        votos_pendentes = self.request.session.get('votos_pendentes', [])
        votos_pendentes.append(voto_data)
        self.request.session['votos_pendentes'] = votos_pendentes

        self.request.session['cargos_votados'] += 1

        pk = self.kwargs['pk']
        cargos = Cargo.objects.filter(eleicao__pk=pk)
        total_cargos = cargos.count()

        if self.request.session['cargos_votados'] >= total_cargos:
            # Save all votes to database
            self._save_all_votes()
            messages.success(self.request, "Todos os votos foram computados com sucesso!")
            # Clear session data
            self.request.session['votos_pendentes'] = []
            self.request.session['cargos_votados'] = 0
            return self.redirect_to_success()
        else:
            # Redirect back to the same view to vote for next position
            return self.redirect_to_next_vote()

    def _save_all_votes(self):
        """Save all pending votes from session to database."""
        try:
            votos_pendentes = self.request.session.get('votos_pendentes', [])

            for voto_data in votos_pendentes:
                Voto.objects.create(
                    eleitor_id=voto_data['eleitor_id'],
                    cargo_id=voto_data['cargo_id'],
                    candidato_id=voto_data['candidato_id'],
                    eleicao_id=voto_data['eleicao_id'],
                    tipo_voto=voto_data['tipo_voto'],
                )
        except Exception as e:
            print(e)
            print(votos_pendentes if votos_pendentes else "Nenhum voto pendente")

    def redirect_to_next_vote(self):
        """Redirect to the same voting view for the next position."""
        from django.http import HttpResponseRedirect
        pk = self.kwargs['pk']
        return HttpResponseRedirect(reverse('votar', kwargs={'pk': pk}))

    def redirect_to_success(self):
        """Redirect to success URL after all votes are saved."""
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(reverse('index'))

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao computar voto.")
        import traceback
        traceback.print_exc()
        print(form.errors.as_data())
        return super().form_invalid(form)

# Class for JavaScript to retrieve a candidate
class BuscarCandidatoView(LoginRequiredMixin, View):
    def get(self, request, eleicao_id, cargo_id, numero):
        candidato = Candidato.objects.filter(cargo__eleicao__pk=eleicao_id, cargo__pk=cargo_id, numero=numero).first()
        if candidato:
            return JsonResponse({
                'candidato': candidato.id,
                'nome': candidato.eleitor.user.username,
                'numero': candidato.numero,
                'foto_url': candidato.foto.url if candidato.foto else None,
                'partido': candidato.partido,
            })
        else:
            return JsonResponse({'candidato': None})