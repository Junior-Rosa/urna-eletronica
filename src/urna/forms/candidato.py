from urna.models import Candidato
from django import forms

class CandidatarForm(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = ['numero', 'partido', 'foto']  # só o que o usuário preenche

        
    

