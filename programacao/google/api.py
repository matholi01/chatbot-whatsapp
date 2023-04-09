import datetime
import os.path
from os import path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

from google.auth.exceptions import MutualTLSChannelError

from datetime import date, timedelta, datetime
import pprint

import pathlib
class Calendario():
    DIR_ATUAL = pathlib.Path(__file__).parent.resolve()

    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    FILE_PATH = path.join(DIR_ATUAL, 'token.json')

    def __init__(self, id_calendario):
        creds = None
        if os.path.exists(self.FILE_PATH):
            creds = service_account.Credentials.from_service_account_file(filename=self.FILE_PATH, scopes=self.SCOPES)    
        try:
            self.service = build('calendar', 'v3', credentials=creds)  
        except Exception:
            raise
                  
        self.id_calendario = id_calendario
        self.timezone = '03:00'
   
    def get_proxima_programacao(self):
        hoje = datetime.now() 
        segunda = hoje - timedelta(days=hoje.weekday())
        segunda = segunda + timedelta(days=7)
        return self._get_programacao(segunda)
    
    def get_atual_programacao(self):
        hoje = datetime.now() 
        segunda = hoje - timedelta(days=hoje.weekday())
        return self._get_programacao(segunda)

    #Retorna a programação dada a data da segunda daquela semana
    def _get_programacao(self,segunda):
        segunda = segunda.replace(hour=00,minute=00,second=00)

        domingo = segunda + timedelta(days=6)
        domingo = domingo.replace(hour=23,minute=59,second=59)
        
        timezone_str = self.timezone
        segunda_str = str(segunda) + '-' + timezone_str
        segunda_str = segunda_str.replace(' ', 'T')

        domingo_str = str(domingo) + '-' + timezone_str
        domingo_str = domingo_str.replace(' ', 'T')

        service = self.service
        events_result = {}

        try:
            events_result = service.events().list(calendarId=self.id_calendario,
                                                    singleEvents=True,
                                                    orderBy='startTime', 
                                                    timeMin=segunda_str,
                                                    timeMax=domingo_str,
                                                    showDeleted=True
                                                ).execute()  
        except Exception:
            raise

        events = events_result.get('items', [])

        programacao_semanal = {
            'ultima_modificacao': None,
            'programacao':[
                {
                    'dia_semana': 'Segunda',
                    'data': segunda.strftime('%d/%m'),
                    'eventos': []
                },
                {
                    'dia_semana': 'Terça',
                    'data': (segunda + timedelta(days=1)).strftime('%d/%m'),
                    'eventos': []
                },
                {
                    'dia_semana': 'Quarta',
                    'data': (segunda + timedelta(days=2)).strftime('%d/%m'),
                    'eventos': []
                },
                {
                    'dia_semana': 'Quinta',
                    'data': (segunda + timedelta(days=3)).strftime('%d/%m'),
                    'eventos': []
                },
                {
                    'dia_semana': 'Sexta',
                    'data': (segunda + timedelta(days=4)).strftime('%d/%m'),
                    'eventos': []
                },
                {
                    'dia_semana': 'Sábado',
                    'data': (segunda + timedelta(days=5)).strftime('%d/%m'),
                    'eventos': []
                },
                {
                    'dia_semana': 'Domingo',
                    'data': (segunda + timedelta(days=6)).strftime('%d/%m'),
                    'eventos': []
                }
            ] 
        }

        programacao = programacao_semanal['programacao']
        ultima_modificacao = datetime(1, 1, 1)
        timezone_horas = datetime.strptime(timezone_str, '%H:%M').hour

        for event in events:

            #Seta ultima modificação na agenda
            data_atualizacao_evento = datetime.strptime(event['updated'], '%Y-%m-%dT%H:%M:%S.%fZ') - timedelta(hours=timezone_horas)

            if ultima_modificacao < data_atualizacao_evento:
                ultima_modificacao = data_atualizacao_evento
            
            if event['status'] == 'cancelled':
                continue

            nome = event['summary']
            date_time = event['start'].get('dateTime')

            horario = ''
            dia_semana = -1

            if date_time != None:
                data_str = date_time.replace('-'+timezone_str,'')
                data_obj = datetime.strptime(data_str, '%Y-%m-%dT%H:%M:%S')
                dia_semana = data_obj.weekday()
                if data_obj.minute == 0:
                    horario = data_obj.strftime('%Hh')
                else:
                    horario = data_obj.strftime('%Hh%M')
            else:
                data = event['start'].get('date')
                data_str = data.replace('-'+timezone_str,'')
                data_obj = datetime.strptime(data_str, '%Y-%m-%d')
                dia_semana = data_obj.weekday()
                horario = '?'

            evento_obj = {'horario': horario, 'nome': nome}

            if dia_semana == 0:
                segunda = programacao[dia_semana]['eventos'] 
                segunda = segunda.append(evento_obj)
            elif dia_semana == 1:
                segunda = programacao[dia_semana]['eventos']  
                segunda = segunda.append(evento_obj)
            elif dia_semana == 2:
                segunda = programacao[dia_semana]['eventos']  
                segunda = segunda.append(evento_obj)
            elif dia_semana == 3:
                segunda = programacao[dia_semana]['eventos']  
                segunda = segunda.append(evento_obj)
            elif dia_semana == 4:
                segunda = programacao[dia_semana]['eventos']  
                segunda = segunda.append(evento_obj)
            elif dia_semana == 5:
                segunda = programacao[dia_semana]['eventos']  
                segunda = segunda.append(evento_obj)
            elif dia_semana == 6:
                segunda = programacao[dia_semana]['eventos']  
                segunda = segunda.append(evento_obj)
        
        programacao_semanal['ultima_modificacao'] = ultima_modificacao.strftime('%d/%m') + ' às ' + ultima_modificacao.strftime('%Hh%M')
        return programacao_semanal

        
    
