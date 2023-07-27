import os
import datetime as dt

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Calendar:
    _creds = None
    _calendar_id: str = "428b4202a71e0d29b1a141655d57bb45eb133fd629e0c84155e1d4bfa7627fa6@group.calendar.google.com"

    @staticmethod
    def _load_credentials() -> None:
        """Загрузка учетных данных из файла "token.json" (если он существует)"""
        if os.path.exists("token.json"):
            Calendar._creds = Credentials.from_authorized_user_file("token.json")

    @staticmethod
    def _get_credentials() -> None:
        """Получение действительных учетных данных или обновление их, если они просрочены"""
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
    def output(cls, events) -> list:
        all_events = []

        if not events:
            print("No upcoming events found")

            return all_events

        for event in events:
            if event['summary'] == "Индивидуальная встреча":
                continue

            events_dict = {}

            start = event["start"].get("dateTime")
            end = event["end"].get("dateTime")

            events_dict["summary"] = event["summary"]
            events_dict["date"] = {
                "day": start[8:10],
                "month": start[5:7],
                "year": start[:4],
            }
            events_dict["startTime"] = start[11:19]
            events_dict["endTime"] = end[11:19]

            all_events.append(events_dict)
        return all_events

    @classmethod
    def check_calendar(cls) -> list or None:
        """Проверяет ближайшие события в календаре с использованием учетных данных Calendar._creds"""
        cls._load_credentials()
        cls._get_credentials()
        try:
            service = build("calendar", "v3", credentials=Calendar._creds)

            now = dt.datetime.now().isoformat() + "Z"

            event_result = service.events().list(
                calendarId=Calendar._calendar_id,
                timeMin=now, maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            ).execute()

            events = event_result.get("items", [])

            return cls.output(events=events)

        except HttpError as error:
            print("An error occurred:", error)

            return

    @classmethod
    def create_calendar_event(cls, data: dict) -> True or None:
        """Создает новое событие в Google Calendar с помощью данных event_data"""
        cls._load_credentials()
        cls._get_credentials()

        event_data: dict = {
            "summary": f"{data['summary']}",
            "location": "Чебоксары",
            "description": f"{data['name']} - {data['phone_number']}",
            "colorId": 9,
            "start": {
                "dateTime": f"{data['start']}",
                "timeZone": "Europe/Moscow"
            },
            "end": {
                "dateTime": f"{data['end']}",
                "timeZone": "Europe/Moscow"
            },
            "recurrence": [
                "RRULE:FREQ=DAILY;COUNT=1"
            ]
        }

        try:
            service = build("calendar", "v3", credentials=Calendar._creds)
            Calendar.delete_event(service=service, start=data['start'], end=data['end'])
            event = service.events().insert(
                calendarId=Calendar._calendar_id,
                body=event_data
            ).execute()
            print(f"Event created: {event.get('htmlLink')}")

            return True

        except HttpError as error:
            print("An error occurred:", error)

            return

    @classmethod
    def delete_event(cls, service, start: str, end: str) -> None:
        events = service.events().list(
            calendarId=Calendar._calendar_id,
            timeMin=start,
            timeMax=end,
            maxResults=10,
            singleEvents=True
        ).execute()

        if 'items' in events:
            for event in events['items']:
                service.events().delete(calendarId=Calendar._calendar_id, eventId=event['id']).execute()
                print(f"Event with ID '{event['id']}' has been deleted.")
        else:
            print("No events found in the specified date and time range.")


data_from_person: dict = {
    "summary": 'Индивидуальная встреча',
    "name": 'Денис',
    "phone_number": '89278685655',
    "start": "2023-07-29T17:00:00+03:00",
    "end": "2023-07-29T18:00:00+03:00",
}

if __name__ == "__main__":
    Calendar.create_calendar_event(data=data_from_person)
    print(Calendar.check_calendar())
