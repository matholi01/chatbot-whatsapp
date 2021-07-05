from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Programacao
from .serializers import *


@api_view(['GET'])
def programacao_list(request):
    if request.method == 'GET':
        data = Programacao.objects.all()

        serializer = ProgramacaoSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)