from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from googleapiclient.errors import HttpError

from .models import Agenda
from .serializers import *

from .google.api import Calendario

@api_view(['GET'])
def programacao_atual(request, semana, igreja):
    agenda_bd = Agenda.objects.filter(igreja__iexact=igreja).first()
    if not agenda_bd:
        return Response({'detalhes': 'A igreja passada na requisição não existe no banco de dados.'},status=status.HTTP_404_NOT_FOUND)
    
    id_calendario = agenda_bd.id_calendario
    agenda = Calendario(id_calendario)
    
    try:
        programacao = []
        if semana == 'atual':
            programacao = agenda.get_atual_programacao()
        elif semana == 'proxima':
            programacao = agenda.get_proxima_programacao()
        else:
            return Response({'detalhes': 'O parâmetro \'semana\' na requisição não corresponde com um nome correto.'}, status.HTTP_400_BAD_REQUEST)
        
        return Response(ProgramacaoSemanalSerializer(programacao).data)
    except HttpError as error:
        return Response({'detalhes': str(error)}, status=error.status_code)
   
    
@api_view(['POST'])
def programacao_mensagem(request):
    agenda = Calendario()
    programacao_semanal = agenda.get_atual_programacao()
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