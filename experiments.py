from datetime import datetime, timedelta
from calendar_api.main import Calendar


def convert_date(date_str):
    # Преобразуем строку в объект datetime
    date_obj = datetime.strptime(date_str, '%d.%m.%Y')

    # Получаем текущую дату и время
    now = datetime.now()

    # Если это сегодняшняя дата, выставляем текущее время
    if date_obj.date() == now.date():
        date_obj = date_obj.replace(hour=now.hour, minute=now.minute, second=now.second)
    else:
        # Если это не сегодня, выставляем полночь
        date_obj = date_obj.replace(hour=0, minute=0, second=0)

    # Преобразуем объект datetime в строку с форматом ISO 8601
    iso_format = date_obj.isoformat()

    return iso_format

date = convert_date("28.07.2023")
print(date)
print(Calendar.check_calendar(date))
