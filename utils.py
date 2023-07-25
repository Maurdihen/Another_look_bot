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


# Примеры использования функции:

