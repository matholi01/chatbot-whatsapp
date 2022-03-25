from datetime import timedelta
from rest_framework import serializers
from .models import Evento

# Retorna o formato de data estabelecido pelo desenvolvedor
def get_data_modificada(data):
    numero_mes = data.month

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

    return data.strftime("%d") + ' ' + meses[numero_mes-1]


class EventoSerializer(serializers.ModelSerializer):

    horario = serializers.SerializerMethodField('get_horario')

    class Meta:
        model = Evento 
        fields = ['nome', 'horario']

    # Retorna o horário em um formato estabelecido pelo desenvolvedor
    def get_horario(self, obj):
        data = obj.data
        # Se for o início de uma hora x, ou seja, 0 minutos de uma hora específica,
        # não é mostrado os minutos.
        if data.minute == 0:
            return obj.data.strftime("%Hh")
        else:
            return obj.data.strftime("%Hh%M")
        

class ProgramacaoSerializer(serializers.Serializer):

    data = serializers.SerializerMethodField('get_data')
    dia_semana = serializers.SerializerMethodField('get_dia_semana')
    eventos = serializers.ListField()

    # Retorna a data modificada
    def get_data(self, obj):
        return get_data_modificada(obj.data)
    
    # Retorna o dia da semana
    def get_dia_semana(self, obj):  
        # 1 = Segunda, 2 = Terça ...
        dia_semana = obj.data.isocalendar()[2]
        dias_semana = ['SEGUNDA','TERÇA','QUARTA','QUINTA','SEXTA','SÁBADO','DOMINGO']

        return dias_semana[dia_semana-1]


class ProgramacaoSemanalSerializer(serializers.Serializer):
    # Nome da igreja daquela programação semanal
    igreja = serializers.SerializerMethodField('get_igreja')

    # Primeiro e último dia de uma programação semanal específica, 
    # ou seja, a segunda e o domingo da próxima semana referente a programação atual. 
    primeiro_dia = serializers.SerializerMethodField('get_segunda')
    ultimo_dia = serializers.SerializerMethodField('get_domingo')

    # Lista de todos os eventos da programação
    programacao = serializers.ListField()

    def get_domingo(self, obj):
        ultimo_dia = obj.data_hoje + timedelta(days=-obj.data_hoje.weekday() + 6)
        return  get_data_modificada(ultimo_dia)

    def get_segunda(self, obj):
        primeiro_dia = obj.data_hoje + timedelta(days=-obj.data_hoje.weekday())
        return get_data_modificada(primeiro_dia)
    
    def get_igreja(self, obj):
        return str(obj.igreja)
    
        