from datetime import datetime

def convert_date(date_str):
    date_obj = datetime.strptime(date_str, '%d.%m.%Y')

    now = datetime.now()

    if date_obj.date() == now.date():
        date_obj = date_obj.replace(hour=now.hour, minute=now.minute, second=now.second)
    else:
        date_obj = date_obj.replace(hour=0, minute=0, second=0)

    iso_format = date_obj.isoformat()

    return iso_format