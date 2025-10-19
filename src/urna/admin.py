from django.contrib import admin
from .models import Eleicao, Cargo, Candidato, Voto, Eleitor 
from .forms import CandidatoForm, VotoForm
# Register your models here.


@admin.register(Eleicao)
class EleicaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'status', 'data_criacao')
    list_filter = ('tipo', 'status')
    search_fields = ('nome',)
    
@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'eleicao', 'digitos')
    list_filter = ('eleicao',)
    search_fields = ('nome',)

@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    form = CandidatoForm
    list_display = ('eleitor', 'numero', 'partido', 'cargo', 'get_votos')
    list_filter = ('cargo__eleicao', 'cargo')
    search_fields = ('eleitor', 'numero', 'partido')
    
    

@admin.register(Eleitor)
class EleitorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'identificador')
    search_fields = ('nome', 'identificador')
    
@admin.register(Voto)
class VotoAdmin(admin.ModelAdmin):
    form = VotoForm
    list_display = ('eleitor', 'candidato', 'data_voto')
    list_filter = ('candidato__cargo__eleicao', 'candidato__cargo')
    search_fields = ('eleitor__nome', 'candidato__nome')
    readonly_fields = ('data_voto',)
    ordering = ('-data_voto',)

    
