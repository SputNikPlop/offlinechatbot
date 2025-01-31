import traceback
import asyncio
from datetime import datetime
import pytz


async def do_timed_event(wait, callback, *args, **kwargs):
    await asyncio.sleep(wait)
    await callback(*args, **kwargs)


def future_callback(future):
    if future.cancelled():
        return
    try:
        result = future.result()
        if result:
            print(result)
    except:
        traceback.print_exc()


def split_message(message):
    messages = []
    while len(message) > 0:
        messages.append(message[:495])
        message = message[495:]
    return messages


def format_date(date):
    time_values = {
        "seconds": ("minutes", 60),
        "minutes": ("hours", 60),
        "hours": ("days", 24),
        "days": ("months", 30),
        "months": ("years", 12),
        "years": ("centuries", 100),
    }
    seconds = (datetime.now(pytz.UTC) - date.replace(tzinfo=pytz.UTC)).total_seconds()
    info = {"seconds": seconds}
    for label, time_value in time_values.items():
        if info[label] >= time_value[1]:
            info[time_value[0]] = info[label] // time_value[1]
            info[label] %= time_value[1]
        else:
            break

    used_info = list(info.keys())[-2:]
    used_info.reverse()

    return " ".join(f"{int(info[label])} {label}" for label in used_info)


def parse_irc_string(string):
    return string.replace(r"\s", " ").replace(r"\:", ";").replace("\\\\", "\\")
