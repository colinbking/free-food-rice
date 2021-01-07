from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class CalendarUpdater():
    def __init__(self):
        self.open_conn = False

    def connect(self):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port) #connect to heroku postgres
        self.cur = conn.cursor()
        self.open_conn = True
    
    def retrieve_events():
        if not self.open_conn:
            self.connect()
        # query db and get events


    def update_cal_all():
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/calendar']

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        events = self.retreive_events()
        for event in events:
            self.update_cal(event)

    def update_cal(self, event):
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        event = {
        'summary': event["food"] + ": " + event["name"],
        'location': event["location"],
        'description': event["desc"],
        'start': {
            'dateTime': '2015-05-28T09:00:00',
            'timeZone': 'America/Chicago',
        },
        'end': {
            'dateTime': '2015-05-28T17:00:00',
            'timeZone': 'America/Chicago',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
            ],
        },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))

        






