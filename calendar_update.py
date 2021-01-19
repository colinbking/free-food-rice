from __future__ import print_function
import datetime
import pickle
import os.path
import psycopg2
import psycopg2.extras
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv, find_dotenv
from urllib.parse import urlparse, unquote
import datetime as dt
from datetime import timedelta
from pytz import timezone


load_dotenv('.env')

class CalendarUpdater():
    def __init__(self):
        self.open_conn = False
        self.month_nums = {"January": 1, "Jan" : 1, "February" : 2, "Feb" :2, "March": 3, "Mar" : 3,  "April" : 4, "Apr" : 4, "May" : 5, "June": 6, "Jun": 6, "July" : 7, "Jul" : 7, "August" : 8, "Aug": 8, "September":  9, "Sep" : 9, "October": 10,"Oct" : 10, "November": 11, "Nov" :11, "December": 12, "Dec":12}


    def connect(self):
        url = urlparse(os.getenv("DATABASE_URL"))
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port) #connect to heroku postgres
        self.open_conn = True
    
    def update_cal_all(self, events):
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

        for event in events:
            if event["food"] == "true":
                self.update_cal(event, service)
    
    def parse_time(self, time_str):
        try:
            tokens = time_str.split(" ")
            print("tokens here:", tokens)
            if len(tokens) <= 11:
                year = int(tokens[3])
                s_month = self.month_nums[tokens[1]]
                s_day = int(tokens[2])
                start_time = int(tokens[5])
                start_ampm = tokens[6]
                end_time = int(tokens[8])
                end_ampm = tokens[9]
                if start_ampm.lower() == "pm":
                    start_time += 12
                if end_ampm.lower() == "pm":
                    end_time += 12
                return dt.datetime(year, s_month, s_day, start_time), dt.datetime(year, s_month, s_day, end_time)

            else:
                year = int(tokens[2])
                s_month = self.month_nums[tokens[0]]
                e_month = self.month_nums[tokens[7]]
                s_day = int(tokens[1])
                e_day = int(tokens[8])
                start_time = int(tokens[4])
                start_ampm = tokens[5]
                end_time = int(tokens[11])
                end_ampm = tokens[12]
                if start_ampm.lower() == "pm":
                    start_time += 12
                if end_ampm.lower() == "pm":
                    end_time += 12
                return dt.datetime(year, s_month, s_day, start_time), dt.datetime(year, e_month, e_day, end_time)
        except Exception as e:
            print(e)
            return(-1, -1)
    




    def update_cal(self, event, service):
        # Use the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        time_str = event["time"]
        start_time, end_time = self.parse_time(time_str)
        event = {
        'summary': event["food"] + ": " + event["name"],
        'location': event["location"],
        'description': event["about"],
        'start': {
            'dateTime': str(start_time.isoformat()),
            'timeZone': 'America/Chicago',
        },
        'end': {
            'dateTime': str(end_time.isoformat()),
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

        


