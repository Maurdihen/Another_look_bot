import os
from pprint import pprint

from googleapiclient.errors import HttpError

from calendar_api.base_calendar import Calendar
from calendar_api.helper import Helper, Id

current_dir = os.path.dirname(os.path.abspath(__file__))
credentials_file_path = os.path.join(current_dir, 'credentials.json')
token_file_path = os.path.join(current_dir, 'token.json')


class GroupCalendar(Calendar):
    _calendar_id: str = "f3670c96d1e99746be552a678e24853f57aeeff498e8556a8942bcbc8dde99b1@group.calendar.google.com"

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
            if len(all_events) == 3:
                break

            if event.get('transparency') == 'transparent':
                event_dict = Helper.create_friendly_event(event)
                all_events.append(event_dict)

        return all_events

    @classmethod
    def check_calendar(cls) -> list or None:
        """
        Проверяет ближайшие события в календаре с использованием учетных данных Calendar._creds
        Returns:
            list or None: Словарь с информацией о ближайших событиях или None, если произошла ошибка.
        """
        with GroupCalendar._get_service(credentials_file_path, token_file_path) as service:
            try:
                time = Helper.find_time_for_group()

                event_result = service.events().list(
                    calendarId=GroupCalendar._calendar_id,
                    timeMin=time.start_time,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                ).execute()

                events = event_result.get('items', [])
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
        with GroupCalendar._get_service(credentials_file_path, token_file_path) as service:
            event_id = cls._get_event_id(start, end, credentials_file_path, token_file_path, GroupCalendar._calendar_id)

            if event_id:
                try:
                    event = service.events().get(calendarId=GroupCalendar._calendar_id, eventId=event_id).execute()

                    current_description = event.get('description', '')
                    new_description = current_description + f"{new_event_data['name']}: " \
                                                            f"{new_event_data['phone_number']}\n"
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
                return Id(**{'event_id': event_id, 'calendar_id': GroupCalendar._calendar_id})
            else:
                print("Event ID not found, nothing has been updated.")

    @classmethod
    def cancel_of_event(cls, event_id: str, user_name: str, user_phone_number: str):
        with GroupCalendar._get_service(credentials_file_path, token_file_path) as service:
            try:
                event = service.events().get(calendarId=GroupCalendar._calendar_id, eventId=event_id).execute()
                new_description = ''
                visitors_amount = 0

                for line in event['description'].splitlines():
                    name, phone_number = line.split()
                    if user_name in name and user_phone_number in phone_number:
                        continue
                    else:
                        new_description += name + ' ' + phone_number + '\n'
                        visitors_amount += 1

                event['description'] = new_description

                if visitors_amount < 5:
                    event['transparency'] = 'transparent'

                updated_event = service.events().update(
                    calendarId=GroupCalendar._calendar_id,
                    eventId=event_id,
                    body=event,
                ).execute()

                print("Event updated:", updated_event.get('htmlLink'))

            except HttpError as error:
                print("An error occurred:", error)


if __name__ == "__main__":
    data = {
        "name": "Ошибка",
        "phone_number": "0190909090",
    }

    pprint(GroupCalendar.check_calendar())
    # GroupCalendar.edit_event(start="2023-08-03T21:00:00+03:00", end="2023-08-03T22:00:00+03:00", new_event_data=data)
    GroupCalendar.cancel_of_event(event_id='4f9m9f114ktti17fdibnsmgneg', user_name='Рома',
                                  user_phone_number='89765965491')
