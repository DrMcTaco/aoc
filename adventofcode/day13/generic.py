from math import gcd
from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


def get_departure_time(arrival_time, schedules):
    departure_time = arrival_time
    buses = [int(schedule) for schedule in schedules.split(",") if schedule != "x"]
    on_bus = False
    while not on_bus:
        for bus in buses:
            if departure_time % bus == 0:
                return departure_time, bus
        departure_time += 1


def lcm(*args):
    val = abs(args[0] * args[1]) // gcd(args[0], args[1])
    if len(args) > 2:
        for i in range(2, len(args)):
            val = abs(val * args[i]) // gcd(val, args[i])

    return val


def check(time, buses):
    checks = []
    for bus in buses:
        checks.append((time + bus[0]) % bus[1] == 0)
    return all(checks)


def get_gold_star(schedules):
    buses = [
        (index, int(schedule))
        for index, schedule in enumerate(schedules.split(","), 0)
        if schedule != "x"
    ]
    step = 1
    time = 1
    for i in range(2, len(buses) + 1):
        while not check(time, buses[0:i]):
            time += step
        step = lcm(*[id[1] for id in buses[0:i]])

    print(f"The gold star time is {time}")


if __name__ == "__main__":
    min_ts, schedules = get_data(day=13, year=2020).splitlines()
    min_ts = int(min_ts)
    departure_time, bus = get_departure_time(min_ts, schedules)
    print(
        f"Wait {departure_time - min_ts} mins for bus id {bus}. Answer: {(departure_time-min_ts) * bus}"
    )
    get_gold_star(schedules)