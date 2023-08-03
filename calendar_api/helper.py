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
    def find_time_for_group(cls, start_time):
        start_time = dt.datetime.fromisoformat(start_time.replace("Z", "+00:00"))
        start_time += dt.timedelta(hours=4)
        start_time = start_time.isoformat()
        return Time(**{"start_time": start_time, "end_time": None})


if __name__ == "__main__":
    time = (Helper.find_time_for_individual("2023-08-03T12:15:00+03:00"))
