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


class GroupCalendar:
    _creds = None
    _calendar_id: str = "f3670c96d1e99746be552a678e24853f57aeeff498e8556a8942bcbc8dde99b1@group.calendar.google.com"

    @staticmethod
    def _load_credentials():
        """Загрузка учетных данных из файла "token.json" (если он существует)"""
        if os.path.exists(token_file_path):
            GroupCalendar._creds = Credentials.from_authorized_user_file(token_file_path)

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

        GroupCalendar._creds = Credentials.from_authorized_user_file(token_file_path,
                                                                     ["https://www.googleapis.com/auth/calendar"])

    @classmethod
    def _output(cls, events: list[dict]) -> list[dict]:
        """
        Преобразует список событий в удобный формат для вывода информации
        Args:
            events (list[dict]): Список словарей с информацией о событиях.
            summary (str): Заголовок события, которое помогает определить идентификатор календаря.
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

        if not events:
            return all_events

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
            events_dict["transparency"] = "transparent"

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
            service = build("calendar", "v3", credentials=GroupCalendar._creds)

            time = Helper.find_time(start_time)

            event_result = service.events().list(
                calendarId=GroupCalendar._calendar_id,
                timeMin=time.start_time,
                timeMax=time.end_time,
                singleEvents=True,
                orderBy="startTime",
            ).execute()

            events = event_result.get("items", [])

            return GroupCalendar._output(events=events)

        except HttpError as error:
            print("An error occurred:", error)
            return


if __name__ == "__main__":
    print(GroupCalendar.check_calendar("2023-08-02T16:59:00+03:00"))