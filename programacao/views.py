from datetime import datetime, timedelta
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .serializers import *

from .google.api import GoogleCalendar

@api_view(['GET'])
def programacao_list(request):
    api = GoogleCalendar()
    return Response(ProgramacaoSemanalSerializer(api.get_atual_programacao()).data)
    
@api_view(['POST'])
def programacao_mensagem(request):
    api = GoogleCalendar()
    programacao_semanal = api.get_atual_programacao()
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