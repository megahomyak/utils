import sys
import select
import datetime
import time

tasks = [
    {"name": f"Task {i}", "time": "8:00"}
    for i in range(1, 28)
]

def now():
    return datetime.datetime.now()

def timedelta_format(td):
    return str(td).split(".")[0]

def update_timer(task_name, remaining_time):
    print("\033[A\033[A")
    print(timedelta_format(now() - global_timer_start_time) + " [" + task_name + " | Time remaining: " + timedelta_format(remaining_time) + "]")

global_timer_start_time = datetime.datetime.now()

def datetime_to_timedelta(dt):
    return datetime.timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)

print()

for task in tasks:
    end_time = now() + datetime_to_timedelta(datetime.datetime.strptime(task["time"], "%M:%S"))
    while now() < end_time:
        remaining_time = end_time - now()
        update_timer(task["name"], remaining_time)
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            key = sys.stdin.readline().strip()
            if key == "":
                break
        time.sleep(1)
