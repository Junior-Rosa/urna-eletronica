from django import forms
from ..models import Candidato, Cargo, Voto, Eleicao

class CandidatoForm(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cargo'].queryset = Cargo.objects.filter(eleicao__status='NAO_INICIADA')
        
    def clean_numero(self):
        numero = self.cleaned_data['numero']
        cargo = self.cleaned_data.get('cargo')
        
        if not cargo:
            raise forms.ValidationError("O cargo deve ser selecionado antes de informar o número.")
        
        if len(numero) != cargo.digitos:
            raise forms.ValidationError(f"O número do candidato deve ter {cargo.digitos} dígitos.")
        return numero
    

class VotoForm(forms.ModelForm):
    class Meta:
        model = Voto
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['eleicao'].queryset = Eleicao.objects.filter(status='EM_ANDAMENTO')
        
        self.fields['cargo'].queryset = Cargo.objects.filter(eleicao__status='EM_ANDAMENTO')
        
    def clean_cargo(self):
        
        if cargo := self.cleaned_data['cargo']:
            if cargo.eleicao != self.cleaned_data.get('eleicao'):
                raise forms.ValidationError(f"Cargo deve ser referente a eleição {cargo} != {self.cleaned_data.get('eleicao')}")
            
        return cargo
    
    def clean_candidato(self):
        if candidato := self.cleaned_data['candidato']:
            if candidato.cargo != self.cleaned_data.get('cargo'):
                raise forms.ValidationError(f"Candidato deve ser referente a cargo {candidato} != {self.cleaned_data.get('cargo')}")
            
        return candidato