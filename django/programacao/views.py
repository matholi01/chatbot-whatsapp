from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Evento
from .serializers import *

from django.db.models import Q

@api_view(['GET'])
def programacao_list(request):
    if request.method == 'GET':
        dados = Evento.objects.all()
        serializer = EventoSerializer(dados, context={'request': request}, many=True)
        return Response(serializer.data)