import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from contextlib import contextmanager

from calendar_api.helper import Helper

current_dir = os.path.dirname(os.path.abspath(__file__))
credentials_file_path = os.path.join(current_dir, 'credentials.json')
token_file_path = os.path.join(current_dir, 'token.json')


class GroupCalendar:
    _scopes = ["https://www.googleapis.com/auth/calendar"]
    _creds = None
    _calendar_id: str = "f3670c96d1e99746be552a678e24853f57aeeff498e8556a8942bcbc8dde99b1@group.calendar.google.com"

    @staticmethod
    def _load_credentials():
        """Загрузка учетных данных из файла "token.json" (если он существует)"""
        if os.path.exists(token_file_path):
            GroupCalendar._creds = Credentials.from_authorized_user_file(token_file_path, GroupCalendar._scopes)

    @staticmethod
    def _get_credentials():
        """Получение действительных учетных данных или обновление их, если они просрочены"""
        if not GroupCalendar._creds or not GroupCalendar._creds.valid:
            if GroupCalendar._creds and GroupCalendar._creds.expired and GroupCalendar._creds.refresh_token:
                GroupCalendar._creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file_path,
                    ["https://www.googleapis.com/auth/calendar"],
                )
                GroupCalendar._creds = flow.run_local_server(port=0)
            with open(token_file_path, "w") as token:
                token.write(GroupCalendar._creds.to_json())

    @staticmethod
    @contextmanager
    def _get_service():
        """Контекстный менеджер для получения сервиса Google Calendar API."""
        GroupCalendar._load_credentials()
        GroupCalendar._get_credentials()
        service = build("calendar", "v3", credentials=GroupCalendar._creds)
        yield service

    @classmethod
    def _get_event_id(cls, start_time: str, end_time: str):
        """
        Возвращает ID первого события, найденного в указанном интервале времени.
        Args:
            start_time (str): Время начала интервала для поиска событий в формате ISO 8601.
            end_time (str): Время окончания интервала для поиска событий в формате ISO 8601.
        Returns:
            str: ID первого найденного события или пустая строка, если события не найдены.
        """
        with GroupCalendar._get_service() as service:
            try:
                events_result = service.events().list(
                    calendarId=GroupCalendar._calendar_id,
                    timeMin=start_time,
                    timeMax=end_time,
                    singleEvents=True,
                    orderBy="startTime",
                ).execute()
                events = events_result.get('items', [])

                if events:
                    return events[0]["id"]
                else:
                    return ""

            except (HttpError, IndexError) as error:
                print("An error occurred:", error)
                return ""

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
            if len(all_events) >= 5:
                break

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
        with GroupCalendar._get_service() as service:
            try:
                time = Helper.find_time(start_time)

                event_result = service.events().list(
                    calendarId=GroupCalendar._calendar_id,
                    timeMin=time.start_time,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                ).execute()

                events = event_result.get("items", [])

                return GroupCalendar._output(events=events)

            except HttpError as error:
                print("An error occurred:", error)
                return

    @classmethod
    def edit_event(cls, start: str, end: str, new_event_data: dict):
        """
        Редактирует событие, найденное в указанном интервале времени, добавляя новую информацию в описание.
        Args:
            start (str): Время начала интервала для поиска события в формате ISO 8601.
            end (str): Время окончания интервала для поиска события в формате ISO 8601.
            new_event_data (dict): Словарь с новыми данными для добавления в описание события.
        """
        with GroupCalendar._get_service() as service:
            event_id = cls._get_event_id(start_time=start, end_time=end)

            if event_id:
                try:
                    event = service.events().get(calendarId=GroupCalendar._calendar_id, eventId=event_id).execute()

                    current_description = event.get('description', '')
                    new_description = current_description + f"{new_event_data['name']}: {new_event_data['phone_number']}\n"
                    event['description'] = new_description

                    visitors_amount = len(event['description'].splitlines())
                    if visitors_amount >= 5:
                        event.pop("transparency")

                    updated_event = service.events().update(
                        calendarId=GroupCalendar._calendar_id,
                        eventId=event_id,
                        body=event,
                    ).execute()

                    print("Event updated:", updated_event.get('htmlLink'))

                except HttpError as error:
                    print("An error occurred:", error)
            else:
                print("Event ID not found, nothing has been updated.")

    @classmethod
    def delete_user_event(cls, eid: str):
        """
        Удаляет событие из Google Calendar по его идентификатору.
        Args:
            eid (str): Идентификатор события, которое нужно удалить.
        Returns:
            None: Функция не возвращает значения.
        """
        with GroupCalendar._get_service() as service:
            try:
                service.events().delete(calendarId=GroupCalendar._calendar_id, eventId=eid).execute()
            except HttpError as error:
                print("An error occurred:", error)


if __name__ == "__main__":
    data = {
        "name": "Ошибка",
        "phone_number": "0190909090",
    }

    print(GroupCalendar.check_calendar(start_time="2023-08-02T00:00:00+03:00"))
    GroupCalendar.edit_event(start="2023-08-03T20:00:00+03:00", end="2023-08-03T21:00:00+03:00", new_event_data=data)
