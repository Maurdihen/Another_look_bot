import os
from pprint import pprint

from googleapiclient.errors import HttpError

from calendar_api.base_calendar import Calendar
from calendar_api.helper import Helper, Id

current_dir = os.path.dirname(os.path.abspath(__file__))
credentials_file_path = os.path.join(current_dir, 'credentials.json')
token_file_path = os.path.join(current_dir, 'token.json')


class IndividualCalendar(Calendar):
    _calendar_id: str = "27e12357628637d37bb635ae2aac09a2c5f2cd48803e2ff583c5c85c3576d93b@group.calendar.google.com"

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
            if event.get('transparency') == 'transparent':
                event_dict = Helper.create_friendly_event(event)
                all_events.append(event_dict)

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
        with IndividualCalendar._get_service(credentials_file_path, token_file_path) as service:
            try:
                time = Helper.find_time_for_individual(start_time)

                event_result = service.events().list(
                    calendarId=IndividualCalendar._calendar_id,
                    timeMin=time.start_time,
                    timeMax=time.end_time,
                    singleEvents=True,
                    orderBy="startTime",
                ).execute()

                events = event_result.get("items", [])

                return IndividualCalendar._output(events=events)

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
        with IndividualCalendar._get_service(credentials_file_path, token_file_path) as service:
            event_id = cls._get_event_id(start_time=start, end_time=end, credentials_file_path=credentials_file_path,
                                         token_file_path=token_file_path, calendar_id=IndividualCalendar._calendar_id)

            if event_id:
                try:
                    event = service.events().get(calendarId=IndividualCalendar._calendar_id, eventId=event_id).execute()

                    new_description = f"{new_event_data['name']}: {new_event_data['phone_number']}"
                    event['description'] = new_description
                    event.pop("transparency")

                    updated_event = service.events().update(
                        calendarId=IndividualCalendar._calendar_id,
                        eventId=event_id,
                        body=event,
                    ).execute()

                    print("Event updated:", updated_event.get('htmlLink'))

                except HttpError as error:
                    print("An error occurred:", error)

                return Id(**{'event_id': event_id, 'calendar_id': IndividualCalendar._calendar_id})
            else:
                print("Event ID not found, nothing has been updated.")

    @classmethod
    def cancel_of_event(cls, event_id: str):
        with IndividualCalendar._get_service(credentials_file_path, token_file_path) as service:
            try:
                event = service.events().get(calendarId=IndividualCalendar._calendar_id, eventId=event_id).execute()
                event['transparency'] = 'transparent'
                new_description = "Человек отменил запись"
                event['description'] = new_description
                updated_event = service.events().update(
                    calendarId=IndividualCalendar._calendar_id,
                    eventId=event_id,
                    body=event,
                ).execute()
                print("Event updated:", updated_event.get('htmlLink'))

            except HttpError as error:
                print("An error occurred:", error)


if __name__ == "__main__":
    data = {
        "name": "Денис",
        "phone_number": "89278685655",
    }

    pprint(IndividualCalendar.check_calendar(start_time="2023-08-16T18:00:00+03:00"))
    # info = IndividualCalendar.edit_event(start="2023-08-08T19:00:00+03:00", end="2023-08-08T20:00:00+03:00",
    #                                      new_event_data=data)
