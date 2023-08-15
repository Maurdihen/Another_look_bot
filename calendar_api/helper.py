import datetime as dt
from dataclasses import dataclass


@dataclass
class Time:
    start_time: str
    end_time: str


@dataclass
class Id:
    event_id: str
    calendar_id: str


class Helper:
    @classmethod
    def find_time_for_individual(cls, start_time):
        # Поиск следующего дня
        next_day = dt.datetime.fromisoformat(start_time[:-6]) + dt.timedelta(days=1)
        end_time = next_day.isoformat() + "+03:00"

        # Поиск сегодняшнего дня
        today = dt.datetime.utcnow() + dt.timedelta(hours=3)
        today = today.isoformat()[8:10]
        day = start_time[8:10]

        if today == day:
            start_time = dt.datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            start_time += dt.timedelta(hours=4)
            start_time = start_time.isoformat()
            # конец дня
            end_time = start_time[:10] + "T23:59:59+03:00"

        return Time(**{"start_time": start_time, "end_time": end_time})

    @classmethod
    def find_time_for_group(cls):
        # start_time = dt.datetime.now()
        # start_time += dt.timedelta(hours=4)
        # or ->
        start_time = dt.datetime.utcnow()
        start_time += dt.timedelta(hours=7)
        start_time = start_time.isoformat()[:19] + '+03:00'
        return Time(**{"start_time": start_time, "end_time": None})

    @classmethod
    def create_friendly_event(cls, event):
        event_dict = {}
        start = event["start"].get("dateTime")
        end = event["end"].get("dateTime")

        event_dict["summary"] = event["summary"]
        event_dict["date"] = {
            "day": start[8:10],
            "month": start[5:7],
            "year": start[:4],
        }
        event_dict["startTime"] = start[11:19]
        event_dict["endTime"] = end[11:19]
        event_dict["event_id"] = event["id"]
        return event_dict

    @classmethod
    def is_cancelable(cls, time):
        current_time = dt.datetime.now(dt.timezone(dt.timedelta(hours=3)))
        tz_offset = current_time.strftime("%z")
        current_time = current_time.strftime("%Y-%m-%d-%H:%M:%S") + f'{tz_offset[:-2]}:{tz_offset[-2:]}'

        current_time = dt.datetime.strptime(current_time, "%Y-%m-%d-%H:%M:%S%z")
        time = dt.datetime.strptime(time, "%Y-%m-%d-%H:%M:%S%z")

        time_diff = time - current_time

        if time_diff < dt.timedelta(hours=24):
            return False
        return True


if __name__ == "__main__":
    print(Helper.is_cancelable("2023-08-16-19:57:40+03:00"))
