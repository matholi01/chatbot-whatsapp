from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from googleapiclient.errors import HttpError

from .models import Agenda, Igreja
from .serializers import *

from .google.api import Calendario

@api_view(['GET'])
def programacao_atual(request, semana, igreja):
    agenda_bd = Agenda.objects.filter(igreja__iexact=igreja).first()
    if not agenda_bd:
        return Response({'detalhes': 'A igreja passada na requisição não existe no banco de dados.'},status=status.HTTP_404_NOT_FOUND)
    
    id_calendario = agenda_bd.id_calendario
    
    try:
        programacao = []
        agenda = Calendario(id_calendario)
        if semana == 'atual':
            programacao = agenda.get_atual_programacao()
        elif semana == 'proxima':
            programacao = agenda.get_proxima_programacao()
        else:
            return Response({'detalhes': 'O parâmetro \'semana\' na requisição não corresponde com um nome correto.'}, status.HTTP_400_BAD_REQUEST)
        
        return Response(ProgramacaoSemanalSerializer(programacao).data)
    except HttpError as error:
        return Response({'detalhes': str(error)}, status=error.status_code)
   
@api_view(['GET'])
def igrejas_mensagem(request):
    igrejas = Agenda.objects.all().order_by('igreja__nome').values_list('igreja__nome',flat=True)

    mensagem = 'Digite o número que corresponde a igreja que você deseja ver a programação:\n'

    for i,igreja in enumerate(igrejas):
        mensagem = mensagem + str(i+1) + ' - ' + igreja + '\n'

    resultado = {'mensagem': mensagem}
    return Response(MensagemSerializer(resultado).data)

@api_view(['GET'])
def igreja_ordem_alfabetica(request, index_alfabetico):
    igrejas = Agenda.objects.all().order_by('igreja__nome').values_list('igreja__nome',flat=True)
    i = index_alfabetico-1
    if i < 0 or i >= len(igrejas):
        return Response({'detalhes': 'Nenhuma igreja corresponde com o index passado.'}, status.HTTP_400_BAD_REQUEST)

    igreja_selecionada = igrejas[i]

    agenda = Agenda.objects.filter(igreja__nome__iexact=igreja_selecionada).first()
    calendario = Calendario(agenda.id_calendario)
    programacao = calendario.get_atual_programacao()

    resultado = _build_mensagem_programacao(programacao)
    return Response(MensagemSerializer(resultado).data)

    
@api_view(['POST'])
def programacao_mensagem(request):
    agenda = Calendario()
    programacao = agenda.get_atual_programacao()
    resultado = _build_mensagem_programacao(programacao)
    return Response(MensagemSerializer(resultado).data)

def _build_mensagem_programacao(programacao):
    todos_eventos = programacao['programacao']
    mensagem = "PROGRAMAÇÃO SEMANAL\n" + todos_eventos[0]['data'] + ' à ' + todos_eventos[6]['data'] + '\n\n'

    for eventos in todos_eventos:
        mensagem = mensagem + eventos['dia_semana'] + ', ' + eventos['data'] + '\n'
        if len(eventos['eventos']) == 0:
            mensagem = mensagem + 'Não há programação.' + '\n\n'
        else:
            for evento in eventos['eventos']:
                mensagem = mensagem + '*' + evento['horario'] + '*' + ': ' + evento['nome'] + '\n'
            mensagem = mensagem + '\n'


    return {'mensagem': mensagem}