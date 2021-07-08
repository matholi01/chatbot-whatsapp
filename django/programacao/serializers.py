from rest_framework import serializers
from .models import Evento

class EventoSerializer(serializers.ModelSerializer):

    dia_semana = serializers.SerializerMethodField('get_dia_semana')
    mes = serializers.SerializerMethodField('get_mes')
    dia = serializers.SerializerMethodField('get_dia')
    horario = serializers.SerializerMethodField('get_horario')

    class Meta:
        model = Evento 
        fields = ('nome','dia','horario','dia_semana','mes')
    
    def get_dia(self, obj):
        return obj.data.day
    
    def get_horario(self, obj):
        return '{hora}h{minuto}'.format(hora = obj.data.hour, minuto = obj.data.minute)

    # Retorna o dia da semana como um inteiro
    # 1 = Janeiro, 2 = Fevereiro ...
    def get_mes(self, obj):
        numero_mes = obj.data.month

        if numero_mes == 1:
            return 'Janeiro'
        elif numero_mes == 2:
            return 'Fevereiro'
        elif numero_mes == 3:
            return 'Março'
        elif numero_mes == 4:
            return 'Abril'
        elif numero_mes == 5:
            return 'Maio'
        elif numero_mes == 6:
            return 'Junho'
        elif numero_mes == 7:
            return 'Julho'
        elif numero_mes == 8:
            return 'Agosto'
        elif numero_mes == 9:
            return 'Setembro'
        elif numero_mes == 10:
            return 'Outubro'
        elif numero_mes == 11:
            return 'Novembro'
        elif numero_mes == 12:
            return 'Dezembro'
                 
    
    # Retorna o dia da semana como um inteiro
    # 1 = Segunda, 2 = Terça ...
    def get_dia_semana(self, obj):
        
        dia_da_semana = obj.data.isocalendar()[2]

        if dia_da_semana == 1:
            return 'Segunda'
        elif dia_da_semana == 2:
            return 'Terça'
        elif dia_da_semana == 3:
            return 'Quarta' 
        elif dia_da_semana == 4:
            return 'Quinta' 
        elif dia_da_semana == 5:
            return 'Sexta' 
        elif dia_da_semana == 6:
            return 'Sábado' 
        elif dia_da_semana == 7:
            return 'Domingo' 


    