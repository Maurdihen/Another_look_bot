import os
from abc import ABC, abstractmethod

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from contextlib import contextmanager

from googleapiclient.errors import HttpError

import utils


class Calendar(ABC):
    _scopes = ["https://www.googleapis.com/auth/calendar"]
    _creds = None
    _calendar_id: str

    @staticmethod
    def _load_credentials(token_file_path):
        """Загрузка учетных данных из файла "token.json" (если он существует)"""
        if os.path.exists(token_file_path):
            Calendar._creds = Credentials.from_authorized_user_file(token_file_path, Calendar._scopes)

    @staticmethod
    def _get_credentials(credentials_file_path, token_file_path):
        """Получение действительных учетных данных или обновление их, если они просрочены"""
        if not Calendar._creds or not Calendar._creds.valid:
            if Calendar._creds and Calendar._creds.expired and Calendar._creds.refresh_token:
                os.remove(token_file_path)
                auth_url, flow, local_server, wsgi_app = utils.create_auth_link(credentials_file_path, utils.data)
                print(auth_url)
                Calendar._creds = utils.run_server(auth_url, flow, local_server, wsgi_app, utils.data)
            else:
                auth_url, flow, local_server, wsgi_app = utils.create_auth_link(credentials_file_path, utils.data)
                print(auth_url)
                Calendar._creds = utils.run_server(auth_url, flow, local_server, wsgi_app, utils.data)

            with open(token_file_path, "w") as token:
                token.write(Calendar._creds.to_json())

    @staticmethod
    @contextmanager
    def _get_service(credentials_file_path, token_file_path):
        """Контекстный менеджер для получения сервиса Google Calendar API."""
        Calendar._load_credentials(token_file_path)
        Calendar._get_credentials(credentials_file_path, token_file_path)
        service = build("calendar", "v3", credentials=Calendar._creds)
        yield service

    @classmethod
    def _get_event_id(cls, start_time: str, end_time: str, credentials_file_path: str, token_file_path: str,
                      calendar_id: str):
        """
        Возвращает ID первого события, найденного в указанном интервале времени.
        Args:
            start_time (str): Время начала интервала для поиска событий в формате ISO 8601.
            end_time (str): Время окончания интервала для поиска событий в формате ISO 8601.
        Returns:
            str: ID первого найденного события или пустая строка, если события не найдены.
        """
        with Calendar._get_service(credentials_file_path, token_file_path) as service:
            try:
                events_result = service.events().list(
                    calendarId=calendar_id,
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
    @abstractmethod
    def edit_event(cls, start: str, end: str, new_event_data: dict):
        pass
