#This program will interact with the schedule of classes API to retrieve and display the status of a specific section.
import requests
import time
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime, time as dtime, timedelta
from zoneinfo import ZoneInfo

URL = "https://classes.rutgers.edu/soc/api/openSections.json"

SECTIONS_TO_WATCH = {  # Section Index : is_open boolean
    "13950" : False,
    "14310" : False,
    "14311" : False,
    "14496" : False,
}

EASTERN = ZoneInfo("America/New_York")
BLACKOUT_START = dtime(2, 0)  # 2:00 AM
BLACKOUT_END = dtime(6, 0)    # 6:00 AM

def get_open_sections(year=2026, term=1, campus="NB"): # For term: 0 = Winter, 1 = Spring, 2 = Summer?, 3 = Fall? Honestly not sure and cannot access SoC to check until they open.
    response = requests.get(
        URL,
        params={"year": year, "term": term, "campus": campus}
    )
    response.raise_for_status()
    return set(response.json())

def watch_sections(indices, interval=60):
  
    print(f"Watching {len(indices)} sections... checking every {interval} seconds.")

    while True:
        now = datetime.now(EASTERN)

        # Respect WebReg downtime
        if in_blackout_window(now):
            sleep_until_morning(now)
            continue

        try:
            open_sections = get_open_sections()

            for key, was_open in indices.items():
                is_open = key in open_sections

                if is_open and not was_open:
                    msg = f"Section {key} is now OPEN!"
                    print(msg)
                    send_push(msg)
                    indices[key] = True
                
                elif not is_open:
                    indices[key] = False

        except Exception as e:
            print(f"Error checking sections: {e}")

        time.sleep(interval)
      
def send_push(message):
    topic = os.environ["NTFY_TOPIC"]
    url = f"https://ntfy.sh/{topic}"

    requests.post(
        url,
        data=message.encode("utf-8"),
        headers={
            "Title": "Rutgers Course Sniper",
            "Priority": "5",
        },
        timeout=10,
    )

def in_blackout_window(now): # Determines if the current time is within the blackout window.
    current_time = now.time()
    return BLACKOUT_START <= current_time < BLACKOUT_END

def sleep_until_morning(now): # Sleeps until the end of the blackout window.
    wake_time = datetime.combine(
        now.date(),
        BLACKOUT_END,
        tzinfo=EASTERN
    )

    # Double checks if it is still sleeping past 6 AM
    if now >= wake_time:
        wake_time += timedelta(days=1)

    seconds = (wake_time - now).total_seconds()
    print(f"WebReg offline. Sleeping until {wake_time.strftime('%I:%M %p')}")
    time.sleep(seconds)

# Example usage:

watch_sections(SECTIONS_TO_WATCH)



