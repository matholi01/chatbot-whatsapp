import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

from datetime import date, timedelta, datetime

import pprint
from collections import OrderedDict

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CALENDAR_ID = '2c6b6ecb318324bbeb7c791211a5f9c755488a68bb7c541c917641a8fab1c981@group.calendar.google.com'

def __get_service():
    path = '/home/matheus/Codigos/programacao-semanal-back/programacao/token.json'
    creds = None
    
    if os.path.exists(path):
        creds = service_account.Credentials.from_service_account_file(filename=path, scopes=SCOPES)    

    return build('calendar', 'v3', credentials=creds)            

def get_programacao_semana_atual():
    hoje = datetime.now() 
    timezone = '03:00'
    segunda = hoje - timedelta(days=hoje.weekday())
    segunda = segunda.replace(hour=00,minute=00,second=00)
    segunda_data_formatada = segunda.strftime('%d/%m')

    domingo = segunda + timedelta(days=6)
    domingo = domingo.replace(hour=23,minute=59,second=59)
    domingo_data_formatada = domingo.strftime('%d/%m')

    segunda_str = str(segunda) + '-' + timezone
    segunda_str = segunda_str.replace(' ', 'T')

    domingo_str = str(domingo) + '-' + timezone
    domingo_str = domingo_str.replace(' ', 'T')

    service = __get_service()


    try:
        events_result = service.events().list(calendarId=CALENDAR_ID,
                                                singleEvents=True,
                                                orderBy='startTime', 
                                                timeMin=segunda_str,
                                                timeMax=domingo_str
                                            ).execute()
        events = events_result.get('items', [])
        

        programacao_semanal = [
            {
                'dia_semana': 'Segunda',
                'data': segunda.strftime('%d/%m'),
                'eventos': []
            },
            {
                'dia_semana': 'Terca',
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
        
        for event in events:
            nome = event['summary']
            data_str = event['start'].get('dateTime').replace('-'+timezone,'')

            data_obj = datetime.strptime(data_str, '%Y-%m-%dT%H:%M:%S')
            
            dia_semana = data_obj.weekday()

            horario = data_obj.strftime('%Hh%M')

            evento_obj = {'nome': nome, 'horario': horario}

            if dia_semana == 0:
                segunda = programacao_semanal[dia_semana]['eventos'] 
                segunda = segunda.append(evento_obj)
            elif dia_semana == 1:
                segunda = programacao_semanal[dia_semana]['eventos']  
                segunda = segunda.append(evento_obj)
            elif dia_semana == 2:
                segunda = programacao_semanal[dia_semana]['eventos']  
                segunda = segunda.append(evento_obj)
            elif dia_semana == 3:
                segunda = programacao_semanal[dia_semana]['eventos']  
                segunda = segunda.append(evento_obj)
            elif dia_semana == 4:
                segunda = programacao_semanal[dia_semana]['eventos']  
                segunda = segunda.append(evento_obj)
            elif dia_semana == 5:
                segunda = programacao_semanal[dia_semana]['eventos']  
                segunda = segunda.append(evento_obj)
            elif dia_semana == 6:
                segunda = programacao_semanal[dia_semana]['eventos']  
                segunda = segunda.append(evento_obj)


        pprint.pprint(programacao_semanal)

        resultado = {'igreja':'Matriz', 
                                'segunda':segunda_data_formatada, 
                                'domingo':domingo_data_formatada, 
                                'programacao':programacao_semanal}

        return resultado
    
    except HttpError as error:
        print('Ocorreu um erro: %s' % error)


if __name__ == '__main__':
    get_programacao_semana_atual()
    #main()
