import os
import datetime as dt

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from calendar_api.helper import Helper

current_dir = os.path.dirname(os.path.abspath(__file__))
credentials_file_path = os.path.join(current_dir, 'credentials.json')
token_file_path = os.path.join(current_dir, 'token.json')


class Calendar:
    _scopes = ["https://www.googleapis.com/auth/calendar"]
    _creds = None
    _calendar_id: str = "27e12357628637d37bb635ae2aac09a2c5f2cd48803e2ff583c5c85c3576d93b@group.calendar.google.com"

    @staticmethod
    def _load_credentials():
        """Загрузка учетных данных из файла "token.json" (если он существует)"""
        if os.path.exists(token_file_path):
            Calendar._creds = Credentials.from_authorized_user_file(token_file_path, Calendar._scopes)

    @staticmethod
    def _get_credentials():
        """Получение действительных учетных данных или обновление их, если они просрочены"""
        if not Calendar._creds or not Calendar._creds.valid:
            if Calendar._creds and Calendar._creds.expired and Calendar._creds.refresh_token:
                Calendar._creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file_path,
                    ["https://www.googleapis.com/auth/calendar"],
                )
                Calendar._creds = flow.run_local_server(port=0)
            with open(token_file_path, "w") as token:
                token.write(Calendar._creds.to_json())

    @classmethod
    def _delete_event(cls, service, start: str, end: str, calendar_id: str):
        """
        Удаляет события из Google Calendar в указанном диапазоне даты и времени.
        Args:
            service: Сервис Google Calendar API, полученный с помощью учетных данных.
            start (str): Начальная дата и время в формате ISO 8601 (например, "2023-07-31T00:00:00+03:00").
            end (str): Конечная дата и время в формате ISO 8601 (например, "2023-07-31T23:59:59+03:00").
            calendar_id (str): Идентификатор календаря, из которого нужно удалить события.
        Returns:
            None: Функция не возвращает значения.
        """
        events = service.events().list(
            calendarId=calendar_id,
            timeMin=start,
            timeMax=end,
            maxResults=10,
            singleEvents=True
        ).execute()

        for event in events.get('items', []):
            service.events().delete(calendarId=calendar_id, eventId=event['id']).execute()
            print(f"Event with ID '{event['id']}' has been deleted.")

        if not events.get('items'):
            print("No events found in the specified date and time range.")

    @classmethod
    def _find_event(cls, service, start: str, end: str, calendar_id: str):
        events = service.events().list(
            calendarId=calendar_id,
            timeMin=start,
            timeMax=end,
            maxResults=1,
            singleEvents=True
        ).execute()

        return events.get('items')['id']

    @classmethod
    def _output(cls, events: list[dict]) -> list[dict]:
        """
        Преобразует список событий в удобный формат для вывода информации
        Args:
            events (list[dict]): Список словарей с информацией о событиях.
        Returns:
            list[dict]: Список словарей с преобразованной информацией о событиях.
            Пример словаря:
                - "summary": Заголовок события.
                - "date": Словарь с информацией о дате события, включающий ключи "day", "month" и "year".
                - "startTime": Время начала события в формате "HH:mm:ss".
                - "endTime": Время окончания события в формате "HH:mm:ss".
                - "transparency": Информация о доступности события (свободен/занят).
        """
        all_events = []

        for event in events:
            transparency = event.get("transparency")

            if transparency is None:
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
            events_dict["transparency"] = transparency

            all_events.append(events_dict)

        return all_events

    @classmethod
    def check_calendar(cls, start_time: str) -> list or None:
        """
        Проверяет ближайшие события в календаре с использованием учетных данных Calendar._creds
        Args:
            start_time (str): Время начала интервала для проверки событий в формате ISO 8601
                              (например, "2023-07-31T00:00:00+03:00").
        Returns:
            list or None: Словарь с информацией о ближайших событиях или None, если произошла ошибка.
        """
        cls._load_credentials()
        cls._get_credentials()

        try:
            service = build("calendar", "v3", credentials=Calendar._creds)

            time = Helper.find_time(start_time)

            event_result = service.events().list(
                calendarId=Calendar._calendar_id,
                timeMin=time.start_time,
                timeMax=time.end_time,
                singleEvents=True,
                orderBy="startTime",
            ).execute()

            events = event_result.get("items", [])

            return Calendar._output(events=events)

        except HttpError as error:
            print("An error occurred:", error)
            return

    @classmethod
    def create_calendar_event(cls, data: dict) -> True or None:
        """
        Создает новое событие в Google Calendar с помощью данных event_data
        Args:
            data (dict): Словарь, включающий ключи "summary", "name", "phone_number", "start", "end",
                         для создания события.
        Returns:
            str or None: Идентификатор созданного события или None, если произошла ошибка.
        """
        cls._load_credentials()
        cls._get_credentials()

        event_data = {
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
            "recurrence": ["RRULE:FREQ=DAILY;COUNT=1"],
        }

        try:
            service = build("calendar", "v3", credentials=Calendar._creds)
            Calendar._delete_event(service=service, start=data['start'], end=data['end'],
                                   calendar_id=Calendar._calendar_id)
            event = service.events().insert(calendarId=Calendar._calendar_id, body=event_data).execute()

            print(f"Event created: {event.get('htmlLink')}")

            return event['id']

        except HttpError as error:
            print("An error occurred:", error)
            return

    @classmethod
    def delete_user_event(cls, eid: str):
        """
        Удаляет событие из Google Calendar по его идентификатору.
        Args:
            eid (str): Идентификатор события, которое нужно удалить.
        Returns:
            None: Функция не возвращает значения.
        """
        cls._load_credentials()
        cls._get_credentials()

        try:
            service = build("calendar", "v3", credentials=Calendar._creds)
            service.events().delete(calendarId=Calendar._calendar_id, eventId=eid).execute()
        except HttpError as error:
            print("error", error)


if __name__ == "__main__":
    data = {"summary": 'Индивидуальная консультация',
            "name": "roma",
            "phone_number": "+79674727177",
            "start": "2023-08-02T18:00:00+03:00",
            "end": "2023-08-02T19:00:00+03:00"}
    print(Calendar.check_calendar(start_time="2023-08-02T16:00:00+03:00"))
