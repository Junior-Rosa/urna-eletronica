# seu_app/forms.py

from django import forms
from .models import Eleicao, Candidato

class EleicaoForm(forms.ModelForm):
    class Meta:
        model = Eleicao
        fields = ['nome', 'tipo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }

class CandidatoForm(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = ['nome', 'numero', 'partido', 'foto', 'cargo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'partido': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        eleicao = kwargs.pop('eleicao', None)
        super().__init__(*args, **kwargs)
        if eleicao:
            # Filtra o campo 'cargo' para mostrar apenas os cargos da eleição atual
            self.fields['cargo'].queryset = eleicao.cargos.all()

class EleitorLoginForm(forms.Form):
    identificador = forms.CharField(label="Seu Identificador (CPF ou Título)", 
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))