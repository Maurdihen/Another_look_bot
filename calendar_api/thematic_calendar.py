import os

from googleapiclient.errors import HttpError

from calendar_api.base_calendar import Calendar
from calendar_api.helper import Helper, Id

current_dir = os.path.dirname(os.path.abspath(__file__))
credentials_file_path = os.path.join(current_dir, 'credentials.json')
token_file_path = os.path.join(current_dir, 'token.json')


class ThematicCalendar(Calendar):
    _calendar_id: str = "961b78b7c2b24064deafd4e8257384fe4afd65cbc8d9ebbc756f3d624d6f175b@group.calendar.google.com"

    @classmethod
    def _output(cls, events: list[dict], subgroup: str) -> list[dict]:
        """
        Преобразует список событий в удобный формат для вывода информации
        Args:
            events (list[dict]): Список словарей с информацией о событиях.
            subgroup (str): Название подкатегории для сортировки вывода по названию мероприятия.
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
        filter_words = ['отношени', 'финанс', 'самореализ']
        filter_word = None

        for word in filter_words:
            if word in subgroup.lower():
                filter_word = word
                break

        for event in events:
            if event.get('transparency') == 'transparent':
                if filter_word is not None and filter_word in event['summary'].lower():
                    event_dict = Helper.create_friendly_event(event)
                    all_events.append(event_dict)

        return all_events

    @classmethod
    def check_calendar(cls, subgroup: str) -> list or None:
        """
        Проверяет ближайшие события в календаре с использованием учетных данных ThematicCalendar._creds
        Args:
            subgroup (str): Название подкатегории для сортировки вывода по названию мероприятия.
        Returns:
            list or None: Словарь с информацией о ближайших событиях или None, если произошла ошибка.
        """
        with ThematicCalendar._get_service(credentials_file_path, token_file_path) as service:
            try:
                time = Helper.find_time_for_group()

                event_result = service.events().list(
                    calendarId=ThematicCalendar._calendar_id,
                    timeMin=time.start_time,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                ).execute()

                events = event_result.get("items", [])

                return ThematicCalendar._output(events=events, subgroup=subgroup)

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
        with ThematicCalendar._get_service(credentials_file_path, token_file_path) as service:
            event_id = cls._get_event_id(start, end, credentials_file_path, token_file_path,
                                         ThematicCalendar._calendar_id)

            if event_id:
                try:
                    event = service.events().get(calendarId=ThematicCalendar._calendar_id, eventId=event_id).execute()

                    current_description = event.get('description', '')
                    new_description = current_description + f"{new_event_data['name']}: " \
                                                            f"{new_event_data['phone_number']}\n"
                    event['description'] = new_description

                    visitors_amount = len(event['description'].splitlines())

                    if visitors_amount >= 5:
                        event.pop("transparency")

                    updated_event = service.events().update(
                        calendarId=ThematicCalendar._calendar_id,
                        eventId=event_id,
                        body=event,
                    ).execute()

                    print("Event updated:", updated_event.get('htmlLink'))

                except HttpError as error:
                    print("An error occurred:", error)
                return Id(**{'event_id': event_id, 'calendar_id': ThematicCalendar._calendar_id})
            else:
                print("Event ID not found, nothing has been updated.")


if __name__ == "__main__":
    data = {'description': 'Денис: 89278685655'}

    print(ThematicCalendar.check_calendar(subgroup="Про самореализацию"))
    # ThematicCalendar.edit_event('2023-08-03T22:30:00+03:00', '2023-08-03T23:30:00+03:00', data)
