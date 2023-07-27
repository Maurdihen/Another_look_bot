import os
import datetime as dt

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Calendar:
    _creds = None

    @staticmethod
    def _load_credentials():
        """Загрузка учетных данных из файла "token.json" (если он существует)."""
        if os.path.exists("token.json"):
            Calendar._creds = Credentials.from_authorized_user_file("token.json")

    @staticmethod
    def _get_credentials():
        """Получение действительных учетных данных или обновление их, если они просрочены."""
        if not Calendar._creds or not Calendar._creds.valid:
            if Calendar._creds and Calendar._creds.expired and Calendar._creds.refresh_token:
                Calendar._creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json",
                                                                 ["https://www.googleapis.com/auth/calendar"])
                Calendar._creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(Calendar._creds.to_json())

    @classmethod
    def create_calendar_event(cls, event_data):
        """
        Создает новое событие в Google Calendar API с помощью данных event_data.
        """
        cls._load_credentials()
        cls._get_credentials()
        try:
            service = build("calendar", "v3", credentials=Calendar._creds)

            event = service.events().insert(
                calendarId='e8738f011308538b82943abd6ce80684786b0c85d7c3a563c0fb5e916c52d051@group.calendar.google.com',
                body=event_data
            ).execute()

            print(f"Event created: {event.get('htmlLink')}")

        except HttpError as error:
            print("An error occurred:", error)

    @classmethod
    def check_calendar(cls):
        """
        Проверяет ближайшие события в календаре "primary" с использованием учетных данных Calendar._creds.
        """
        cls._load_credentials()
        cls._get_credentials()
        try:
            service = build("calendar", "v3", credentials=Calendar._creds)

            now = dt.datetime.now().isoformat() + "Z"

            event_result = service.events().list(
                calendarId="primary",
                timeMin=now, maxResults=10,
                singleEvents=True,
                orderBy="startTime"
            ).execute()

            events = event_result.get("items", [])

            if not events:
                print("No upcoming events found!")
                return

            print("Upcoming events:")
            for event in events:
                # print(event)
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])

        except HttpError as error:
            print("An error occurred:", error)


# name, phone number, start-end, summary
if __name__ == "__main__":
    event_data = {
        "summary": "Индивидуальная встреча",
        "location": "Чебоксары",
        "description": "Проблемы с личной жизнью",
        "colorId": 5,
        "start": {
            "dateTime": "2023-07-25T17:30:00+03:00",
            "timeZone": "Europe/Moscow"
        },
        "end": {
            "dateTime": "2023-07-25T19:30:00+03:00",
            "timeZone": "Europe/Moscow"
        },
        "recurrence": [
            "RRULE:FREQ=DAILY;COUNT=1"
        ],
        # "attendees": [
        #     {"email": "pashenka.kuzmin.2006@gmail.com"},
        # ],
    }

    # Создание события в календаре
    # Calendar.create_calendar_event(event_data)
    # Просмотр календаря
    # Calendar.check_calendar()
