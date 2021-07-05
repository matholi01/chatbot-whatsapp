from rest_framework import serializers
from .models import Programacao

class ProgramacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Programacao 
        fields = ('nome', 'data')