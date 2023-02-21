# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START calendar_quickstart]
from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():

    path = "chaves/programacao-semanal-develop-4824e9a71212.json"

    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(path):
        creds = service_account.Credentials.from_service_account_file(filename=path, scopes=SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open(path, 'w') as token:
    #         token.write(creds.to_json())
    
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        #print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='2c6b6ecb318324bbeb7c791211a5f9c755488a68bb7c541c917641a8fab1c981@group.calendar.google.com',
                                              singleEvents=True,
                                              orderBy='startTime', 
                                              timeMin='2023-02-20T00:00:00-03:00',
                                              timeMax='2023-02-26T23:59:00-03:00').execute()
        events = events_result.get('items', [])

        #events = service.calendarList().list().execute()

        if not events:
            print('No upcoming events found.')
            return

        #Prints the start and name of the next 10 events
        #print(events)
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
# [END calendar_quickstart]