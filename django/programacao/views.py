from datetime import datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Evento
from .serializers import *

@api_view(['GET'])
def programacao_list(request):
    if request.method == 'GET':
        # Lista com os eventos de um dia da semana
        eventos_dia_semana = []

        # Lista de eventos de um dia da semana "serializados"
        serializer = []

        # Lista com todos os eventos da semana serializados
        resposta = []

        # Eventos da semana atual
        dados_semana_atual = Evento.objects.filter(data__week = datetime.today().isocalendar()[1])
        
        for i,n in enumerate(list(range(1,8))):
            # Filtra a partir do número da dia da semana. Começa na segunda e termina no domingo.
            eventos_dia_semana.append(dados_semana_atual.filter(data__week_day=n%7+1)) 

            serializer.append(EventoSerializer(eventos_dia_semana[i], context={'request': request}, many=True).data)
            resposta.append(serializer[i])
    
        return Response(resposta)