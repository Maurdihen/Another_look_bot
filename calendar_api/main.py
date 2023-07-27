import os.path
import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Область доступа к Google Calendar API
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def check():
    """
    Функция для проверки учетных данных и создания клиента API Google Calendar.

    Returns:
        service (googleapiclient.discovery.Resource): Клиент API Google Calendar, инициализированный с действующими учетными данными.

    Результат:
        Возвращает объект клиента API Google Calendar или None, если произошла ошибка при создании клиента.
    """

    # Инициализируем переменную creds как None
    creds = None

    # Проверяем, существует ли файл токена "token.json"
    if os.path.exists("token.json"):
        # Если существует, загружаем учетные данные из файла
        creds = Credentials.from_authorized_user_file("token.json")

    # Если учетные данные отсутствуют или истек срок действия
    if not creds or not creds.valid:
        # Если учетные данные содержат обновляемый токен, обновляем их
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        # В противном случае выполняем процесс аутентификации
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Сохраняем учетные данные в файл "token.json"
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Создаем клиент API Google Calendar с помощью полученных учетных данных
        service = build("calendar", "v3", credentials=creds)
        return service
    except HttpError:
        return None


def create_event():
    """
    Функция для создания нового события в календаре "primary" (основной календарь пользователя).

    Returns:
        None

    Результат:
        Создает новое событие в календаре и выводит ссылку на созданное событие на экран.
    """

    # Проверяем учетные данные и получаем объект клиента API Google Calendar
    service = check()

    try:
        # Создаем словарь с информацией о событии, которое нужно создать
        event = {
            "summary": "My python event",
            "location": "somewhere",
            "description": "some details",
            "colorId": 2,
            "start": {
                "dateTime": "2023-07-26T17:30:00+03:00",
                "timeZone": "Europe/Moscow"
            },
            "end": {
                "dateTime": "2023-07-26T19:30:00+03:00",
                "timeZone": "Europe/Moscow"
            },
            "recurrence": [
                "RRULE:FREQ=DAILY;COUNT=1"
            ],
            "attendees": [
                {"email": "social@neuralnine.com"},
                {"email": "someemailthathopefullydoesnotexist@mail.com"}
            ]
        }

        # Вставляем событие в календарь "primary" с помощью метода insert()
        event = service.events().insert(calendarId='primary', body=event).execute()

        # Выводим ссылку на созданное событие
        print(f"event created {event.get('htmlLink')}")

    # Обрабатываем ошибки HttpError
    except HttpError as error:
        print("An error occurred:", error)


def print_events():
    """
    Функция для вывода списка предстоящих событий из календаря "primary" (основной календарь пользователя).

    Returns:
        None

    Результат:
        Выводит на экран список предстоящих событий, включающий время начала и заголовок события.
    """

    # Проверяем учетные данные и получаем объект клиента API Google Calendar
    service = check()

    # Получаем текущую дату и время в формате ISO 8601
    now = dt.datetime.now().isoformat() + "Z"

    # Получаем список предстоящих событий из календаря "primary" с использованием объекта клиента API
    event_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    # Извлекаем список событий из результата запроса
    events = event_result.get("items", [])

    # Если список событий пуст, выводим сообщение о его отсутствии и завершаем функцию
    if not events:
        print("No upcoming events found!")
        return

    # Выводим информацию о каждом предстоящем событии
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])


# Если код запущен как самостоятельный скрипт
if __name__ == "__main__":
    create_event()
    print_events()
