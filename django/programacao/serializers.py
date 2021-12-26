from rest_framework import serializers
from .models import Evento


class EventoSerializer(serializers.ModelSerializer):

    horario = serializers.SerializerMethodField('get_horario')

    class Meta:
        model = Evento 
        fields = ['nome', 'horario']

    def get_horario(self, obj):
        return obj.data.strftime("%Hh%M")

class ProgramacaoSerializer(serializers.Serializer):

    dia = serializers.SerializerMethodField('get_dia')
    mes = serializers.SerializerMethodField('get_mes')
    dia_semana = serializers.SerializerMethodField('get_dia_semana')
    eventos = serializers.ListField()

    def get_dia(self, obj):
        return obj.data.day  
    
    # Retorna o dia da semana como um inteiro
    # 1 = Janeiro, 2 = Fevereiro ...
    def get_mes(self, obj):
        numero_mes = obj.data.month

        meses = ['JAN', 
            'FEV', 
            'MAR', 
            'ABRIL', 
            'MAIO', 
            'JUN', 
            'JUL', 
            'AGO',
            'SET', 
            'OUT', 
            'NOV', 
            'DEZ'
        ]

        dicio_meses = {}
        for i in range(12):
            dicio_meses[i+1] = meses[i]

        return dicio_meses[numero_mes]
    
    # Retorna o dia da semana como um inteiro
    # 1 = Segunda, 2 = Terça ...
    def get_dia_semana(self, obj):
        
        dia_semana = obj.data.isocalendar()[2]
        semana = ['Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo']

        dicio_dia_semana = {}
        for i in range(7):
            dicio_dia_semana[i+1] = semana[i]

        return dicio_dia_semana[dia_semana]
