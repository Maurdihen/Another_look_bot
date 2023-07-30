import os
import datetime as dt

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

current_dir = os.path.dirname(os.path.abspath(__file__))
credentials_file_path = os.path.join(current_dir, 'credentials.json')
token_file_path = os.path.join(current_dir, 'token.json')


class Calendar:
    _creds = None
    # идентификатор календаря для индивидуальных занятий
    _in_calendar_id: str = "27e12357628637d37bb635ae2aac09a2c5f2cd48803e2ff583c5c85c3576d93b@group.calendar.google.com"
    # идентификатор календаря для групповых занятий
    _gr_calendar_id: str = "f3670c96d1e99746be552a678e24853f57aeeff498e8556a8942bcbc8dde99b1@group.calendar.google.com"

    @staticmethod
    def _load_credentials() -> None:
        """Загрузка учетных данных из файла "token.json" (если он существует)"""
        if os.path.exists(token_file_path):
            Calendar._creds = Credentials.from_authorized_user_file(token_file_path)

    @staticmethod
    def _get_credentials() -> None:
        """Получение действительных учетных данных или обновление их, если они просрочены"""
        if not Calendar._creds or not Calendar._creds.valid:
            if Calendar._creds and Calendar._creds.expired and Calendar._creds.refresh_token:
                Calendar._creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file_path,
                                                                 ["https://www.googleapis.com/auth/calendar"])
                Calendar._creds = flow.run_local_server(port=0)
            with open(token_file_path, "w") as token:
                token.write(Calendar._creds.to_json())

    @classmethod
    def _output(cls, events: list[dict]) -> list[dict]:
        """Преобразует список событий в удобный формат для вывода информации"""
        all_events = []

        if not events:
            return []

        for event in events:
            transparency = event.get("transparency")

            if transparency is None:
                continue
            else:
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
                events_dict["transparency"] = transparency

                all_events.append(events_dict)

        return all_events

    @classmethod
    def check_calendar(cls, start_time) -> dict or None:
        """Проверяет ближайшие события в календаре с использованием учетных данных Calendar._creds"""
        cls._load_credentials()
        cls._get_credentials()
        try:

            service = build("calendar", "v3", credentials=Calendar._creds)

            next_day = dt.datetime.fromisoformat(start_time[:-6]) + dt.timedelta(days=1)
            end_time = next_day.isoformat() + "+03:00"

            today = dt.datetime.utcnow().isoformat()[8:10]
            day = start_time[8:10]

            if today == day:
                end_time = start_time[:10] + "T" + "23:59:59" + "+03:00"

            event_result = service.events().list(
                calendarId=Calendar._in_calendar_id,
                timeMin=start_time,
                timeMax=end_time,
                singleEvents=True,
                orderBy="startTime",
            ).execute()

            events = event_result.get("items", [])

            return Calendar._output(events)

        except HttpError as error:
            print("An error occurred:", error)
            return

    @classmethod
    def create_calendar_event(cls, data: dict) -> True or None:
        """
        Создает новое событие в Google Calendar с помощью данных event_data
        data = {
            "summary": 'Индивидуальная встреча',
            "name": 'Денис',
            "phone_number": '89278685655',
            "start": "2023-07-29T18:00:00+03:00",
            "end": "2023-07-29T19:00:00+03:00",
            }
        """
        cls._load_credentials()
        cls._get_credentials()

        # if data['summary'] == 'Индивидуальная встреча':
        #     calendar_id = Calendar._in_calendar_id
        # elif data['summary'] == 'Групповые занятия':
        #     calendar_id = Calendar._gr_calendar_id

        event_data: dict = {
            "summary": f"{data['summary']}",
            "location": "Чебоксары",
            "description": f"{data['name']} - {data['phone_number']}",
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
            ],
        }

        try:
            service = build("calendar", "v3", credentials=Calendar._creds)
            Calendar._delete_event(service=service, start=data['start'], end=data['end'])
            event = service.events().insert(
                calendarId=Calendar._in_calendar_id,
                body=event_data
            ).execute()

            print(f"Event created: {event.get('htmlLink')}")

            return event['id']

        except HttpError as error:
            print("An error occurred:", error)

            return

    @classmethod
    def _delete_event(cls, service, start: str, end: str) -> None:
        events = service.events().list(
            calendarId=Calendar._in_calendar_id,
            timeMin=start,
            timeMax=end,
            maxResults=10,
            singleEvents=True
        ).execute()

        if 'items' in events:
            for event in events['items']:
                service.events().delete(calendarId=Calendar._in_calendar_id, eventId=event['id']).execute()
                print(f"Event with ID '{event['id']}' has been deleted.")
        else:
            print("No events found in the specified date and time range.")

    @classmethod
    def delete_user_event(cls, eid: str):
        cls._load_credentials()
        cls._get_credentials()
        try:
            service = build("calendar", "v3", credentials=Calendar._creds)
            service.events().delete(calendarId=Calendar._in_calendar_id, eventId=eid).execute()
        except HttpError as error:
            print("error", error)


if __name__ == "__main__":
    print(Calendar.check_calendar("2023-07-31T00:00:00+03:00"))