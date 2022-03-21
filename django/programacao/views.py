from datetime import date, datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Evento, Igreja
from .serializers import *

# Ajuda na modificação do retorno da requição GET
class ProgramacaoDia:
    def __init__(self, data, eventos):
        # Eventos de um dia da semana de uma certa semana
        self.eventos = eventos
        # Data do dia da semana de uma certa semana
        self.data = data

@api_view(['GET'])
def programacao_list(request, igreja):
    if request.method == 'GET':

        # Checa se existe uma igreja cadastrada com esse nome. Se não tiver, terminamos.
        # iexact serve para a consulta corresponder exatamente com o nome da igreja salva no Banco de dados
        # e para não distinguir entre caracteres maiúsculos e minúsculos (Case-insensitive)
        if not Igreja.objects.filter(nome__iexact=igreja):
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Número da semana atual
        num_semana = datetime.today().isocalendar()[1]


        # Eventos da semana atual e igreja passada como parâmetro
        eventos = Evento.objects.filter(data__week=num_semana, igreja__nome__iexact=igreja)

        # Guardará a programação completa de uma semana
        programacao_serializada = []

        for i in range(1,8):
            # Eventos do dia da semana i.
            # 1 <= i <= 7 e significa Segunda, Terça, ..., Domingo 
            eventos_dia = eventos.filter(data__iso_week_day=i).order_by('data')

            # Se existe um evento no dia da semana i na semana atual
            if eventos_dia.exists():
                # Serializa os eventos
                eventos_serializados = EventoSerializer(eventos_dia, many=True).data 

                # Guarda a data do dia da semana daquela semana
                data = eventos_dia.values('data').first().get('data')

                # Utiliza um objeto para modificar o retorno da requisição GET
                programacao_dia = ProgramacaoDia(data=data, eventos=eventos_serializados)

                # Inclui na lista a programação de um dia da semana i da semana atual
                programacao_serializada.append(ProgramacaoSerializer(programacao_dia).data)

    return Response(programacao_serializada)