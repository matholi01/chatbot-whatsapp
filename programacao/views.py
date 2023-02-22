from datetime import datetime, timedelta
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Evento, Igreja
from .serializers import *

from .api import *

# Ajuda na serialização. Também modifica o retorno da requisição GET.
class ProgramacaoDia:
    def __init__(self, data, eventos):
        # Eventos de um dia da semana de uma certa semana
        self.eventos = eventos
        # Data do dia da semana de uma certa semana
        self.data = data

# Ajuda na serialização. Também modifica o retorno da requisição GET.
class ProgramacaoSemanal:
    def __init__(self, programacao, data_hoje, igreja):
        # Eventos de uma programação semanal
        self.programacao = programacao
        # Data de hoje
        self.data_hoje = data_hoje
        # Nome da igreja
        self.igreja = igreja

@api_view(['GET'])
def programacao_list(request):
    return Response(ProgramacaoSemanalSerializer(get_programacao_semana_atual()).data)
    
@api_view(['POST'])
def programacao_mensagem(request):
    programacao_semanal = get_programacao_semana_atual()
    todos_eventos = programacao_semanal['programacao']
    mensagem = "PROGRAMAÇÃO SEMANAL\n" + programacao_semanal['segunda'] + ' à ' + programacao_semanal['domingo'] + '\n\n'

    for eventos in todos_eventos:
        mensagem = mensagem + eventos['dia_semana'] + ', ' + eventos['data'] + '\n'
        if len(eventos['eventos']) == 0:
            mensagem = mensagem + 'Não há programação.' + '\n\n'
        else:
            for evento in eventos['eventos']:
                mensagem = mensagem + '*' + evento['horario'] + '*' + ': ' + evento['nome'] + '\n'
            mensagem = mensagem + '\n'


    resultado = {'mensagem': mensagem}
    return Response(ProgramacaoSemanalMensagemSerializer(resultado).data)