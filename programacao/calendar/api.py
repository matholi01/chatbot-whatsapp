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

def get_service():
    path = "token.json"
    creds = None
    
    if os.path.exists(path):
        creds = service_account.Credentials.from_service_account_file(filename=path, scopes=SCOPES)    

    return build('calendar', 'v3', credentials=creds)            

def get_eventos_semana_atual():
    hoje = datetime.now() 
    timezone = '03:00'
    segunda = hoje - timedelta(days=hoje.weekday())
    segunda = segunda.replace(hour=00,minute=00,second=00)

    domingo = segunda + timedelta(days=6)
    domingo = domingo.replace(hour=23,minute=59,second=59)

    segunda = str(segunda) + '-' + timezone
    segunda = segunda.replace(' ', 'T')

    domingo = str(domingo) + '-' + timezone
    domingo = domingo.replace(' ', 'T')

    print(segunda)
    print(domingo)

    service = get_service()


    try:
        events_result = service.events().list(calendarId=CALENDAR_ID,
                                                singleEvents=True,
                                                orderBy='startTime', 
                                                timeMin=segunda,
                                                timeMax=domingo
                                            ).execute()
        events = events_result.get('items', [])

        programacao_semanal = OrderedDict(
            segunda=[],
            terca=[],
            quarta=[],
            quinta=[],
            sexta=[],
            sabado=[],
            domingo=[]
        )

        
        for event in events:
            nome = event['summary']
            data_str = event['start'].get('dateTime').replace('-'+timezone,'')

            data_obj = datetime.strptime(data_str, '%Y-%m-%dT%H:%M:%S')
            dia_semana = data_obj.weekday()

            data_formatada = data_obj.strftime('%d/%m')
            horario = data_obj.strftime('%Hh%M')

            evento_obj = {'nome': nome, 'data': data_formatada, 'horario': horario}

            if dia_semana == 0:
                segunda = programacao_semanal['segunda'] 
                segunda = segunda.append(evento_obj)
            elif dia_semana == 1:
                segunda = programacao_semanal['terca'] 
                segunda = segunda.append(evento_obj)
            elif dia_semana == 2:
                segunda = programacao_semanal['quarta'] 
                segunda = segunda.append(evento_obj)
            elif dia_semana == 3:
                segunda = programacao_semanal['quinta'] 
                segunda = segunda.append(evento_obj)
            elif dia_semana == 4:
                segunda = programacao_semanal['sexta'] 
                segunda = segunda.append(evento_obj)
            elif dia_semana == 5:
                segunda = programacao_semanal['sabado'] 
                segunda = segunda.append(evento_obj)
            elif dia_semana == 6:
                segunda = programacao_semanal['domingo'] 
                segunda = segunda.append(evento_obj)


        pprint.pprint(programacao_semanal)
        return events
    
    except HttpError as error:
        print('Ocorreu um erro: %s' % error)


# if __name__ == '__main__':
#     get_eventos_semana_atual()
#     #main()
