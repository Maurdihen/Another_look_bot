from datetime import datetime, timedelta


def get_start_end_of_week(next_week=False):
    today = datetime.today()

    if next_week:
        start_date = today + timedelta(days=7)
        end_date = start_date + timedelta(days=6)
    else:
        start_date = today
        end_date = start_date + timedelta(days=6)

    return f"{start_date.strftime('%d.%m')} - {end_date.strftime('%d.%m')}"


def convert_date(date_str):
    date_obj = datetime.strptime(date_str, '%d.%m.%Y')

    now = datetime.now()

    if date_obj.date() == now.date():
        date_obj = date_obj.replace(hour=now.hour, minute=now.minute, second=now.second)
    else:
        date_obj = date_obj.replace(hour=0, minute=0, second=0)

    iso_format = date_obj.isoformat()

    return iso_format