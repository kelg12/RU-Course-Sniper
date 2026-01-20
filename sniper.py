#This program will interact with the schedule of classes API to retrieve and display the status of a specific section.
import requests
import time
import os
import json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime, time as dtime, timedelta
from zoneinfo import ZoneInfo

URL = "https://classes.rutgers.edu/soc/api/openSections.json"

CONFIG_PATH = Path(__file__).parent / "config.json"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def initialize_sections(config):
    return {section: False for section in config["sections"]}

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
  
    print(f"Watching {len(indices)} sections... checking every {interval} seconds.", flush=True)

    while True:
        now = datetime.now(EASTERN)

        # Respect WebReg downtime
        if in_blackout_window(now):
            sleep_until_morning(now)
            continue

        try:
            open_sections = get_open_sections()

            print(
                f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] "
                f"Checked {len(indices)} sections, "
                f"{len(open_sections)} currently open",
                flush=True
            )
            

            for key, was_open in indices.items():
                is_open = key in open_sections

                if is_open and not was_open:
                    msg = f"Section {key} is now OPEN!"
                    print(msg, flush=True)
                    send_push(msg, flush=True)
                    indices[key] = True
                
                elif not is_open:
                    indices[key] = False

        except Exception as e:
            print(f"Error checking sections: {e}", flush=True)

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
    print(f"WebReg offline. Sleeping until {wake_time.strftime('%I:%M %p')}", flush=True)
    time.sleep(seconds)

def main(): # Main function loads config file and starts watching sections.
    config = load_config()

    poll_interval = config.get("poll_interval", 60)
    sections = initialize_sections(config)

    if not sections:
        raise RuntimeError("No sections configured to watch. Please add sections in config.json.")
    
    watch_sections(sections, interval=poll_interval)

if __name__ == "__main__":
    main()




