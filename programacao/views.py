from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from googleapiclient.errors import HttpError

from .models import Agenda
from .serializers import *

from .google.api import Calendario

@api_view(['GET'])
def programacao_igreja_bruto(request, semana, igreja):
    agenda_bd = Agenda.objects.filter(igreja__nome__iexact=igreja).first()
    if not agenda_bd:
        return Response({'erro': 'A igreja passada na requisição não existe no banco de dados.'},
                        status=status.HTTP_404_NOT_FOUND)
    
    id_calendario = agenda_bd.id_calendario
    
    try:
        programacao = []
        calendario = Calendario(id_calendario)
        if semana == 'atual':
            programacao = calendario.get_atual_programacao()
        elif semana == 'proxima':
            programacao = calendario.get_proxima_programacao()
        else:
            return Response({'erro': 'O parâmetro \'semana\' na requisição não corresponde com um nome correto.'}, 
                            status.HTTP_400_BAD_REQUEST)
        
        return Response(ProgramacaoSemanalSerializer(programacao).data)
    except Exception as error:
        return Response({'erro': 'Houve um erro ao retornar a programação semanal dessa igreja'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
@api_view(['POST'])
def igrejas_mensagem(request):
    igrejas = Agenda.objects.all().order_by('igreja__nome').values_list('igreja__nome',flat=True)

    if not igrejas:
        return Response({'erro': 'Nenhuma agenda foi encontrada.'}, status=status.HTTP_404_NOT_FOUND)

    mensagem = ''

    for i,igreja in enumerate(igrejas):
        mensagem = mensagem + '*' + str(i+1) + '*: ' + igreja + '\n'

    resultado = {'mensagem': mensagem}
    return Response(MensagemSerializer(resultado).data)

@api_view(['POST'])
def programacao_igreja_mensagem(request, semana):
    index_alfabetico = request.data.get('index_alfabetico')
    if index_alfabetico is None:
        return Response({'erro': 'O campo \'index_alfabetico\' não foi encontrado no body da requisição.'}, 
                        status.HTTP_400_BAD_REQUEST) 
    elif not index_alfabetico.isdigit():
        return Response({'erro': 'O campo \'index_alfabetico\' deve ser um número inteiro.'}, 
                        status.HTTP_406_NOT_ACCEPTABLE)

    igrejas = Agenda.objects.all().order_by('igreja__nome').values_list('igreja__nome',flat=True)
    index_alfabetico = int(index_alfabetico)

    i = index_alfabetico-1
    if i < 0 or i >= len(igrejas):
        return Response({'erro': 'Nenhuma igreja corresponde com o index passado.'}, 
                        status.HTTP_404_NOT_FOUND)

    igreja_selecionada = igrejas[i]
    agenda = Agenda.objects.filter(igreja__nome__iexact=igreja_selecionada).first()
    programacao = []
    try:
        calendario = Calendario(agenda.id_calendario)
        if semana == 'atual':
            programacao = calendario.get_atual_programacao()
        elif semana == 'proxima':
            programacao = calendario.get_proxima_programacao()
        else:
            return Response({'erro': 'O parâmetro \'semana\' na requisição não corresponde com um nome correto.'}, status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({'erro': 'Houve um erro ao retornar a programação semanal dessa igreja'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    resultado = _build_mensagem_programacao(programacao, igreja_selecionada)
    return Response(MensagemSerializer(resultado).data)

def _build_mensagem_programacao(programacao, igreja):
    todos_eventos = programacao['programacao']
    mensagem = 'Programação Semanal:\n' + '*' + igreja + '*' + '\n' + todos_eventos[0]['data'] + ' à ' + todos_eventos[6]['data'] + '\n\n'

    for eventos in todos_eventos:
        mensagem = mensagem + '*' + eventos['dia_semana'] + '*' + ', ' + eventos['data'] + '\n'
        if not eventos['eventos']:
            mensagem = mensagem + '_Não há programação._' + '\n\n'
        else:
            for evento in eventos['eventos']:
                mensagem = mensagem + '*' + evento['horario'] + '*' + ': ' + evento['nome'] + '\n\n'

    # Retira o último \n da mensagem
    mensagem = mensagem.rstrip(mensagem[-1])
    
    return {'mensagem': mensagem}