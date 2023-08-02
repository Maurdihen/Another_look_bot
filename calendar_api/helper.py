import datetime as dt
from dataclasses import dataclass


@dataclass
class Time:
    start_time: str
    end_time: str


class Helper:
    @classmethod
    def find_time(cls, start_time):
        # Поиск следующего дня
        next_day = dt.datetime.fromisoformat(start_time[:-6]) + dt.timedelta(days=1)
        end_time = next_day.isoformat() + "+03:00"

        # Поиск сегодняшнего дня
        today = dt.datetime.utcnow().isoformat()[8:10]
        day = start_time[8:10]

        if today == day:
            # нельзя записаться за 3 часа до ивента
            start_time = dt.datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            start_time += dt.timedelta(hours=4)
            start_time = start_time.isoformat()
            # конец дня
            end_time = start_time[:10] + "T23:59:59+03:00"

        return Time(**{"start_time": start_time, "end_time": end_time})


if __name__ == "__main__":
    time = (Helper.find_time("2023-08-02T16:15:00+03:00"))
    print(time.start_time)
