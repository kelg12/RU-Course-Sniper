#This program will interact with the schedule of classes API to retrieve and display the status of a specific section.
import requests
import time
import os
from dotenv import load_dotenv
load_dotenv()

URL = "https://classes.rutgers.edu/soc/api/openSections.json"

SECTIONS_TO_WATCH = {
    "13950" : False,
    "14310" : False,
    "14311" : False,
    "14496" : False,
}

def get_open_sections(year=2026, term=1, campus="NB"):
    response = requests.get(
        URL,
        params={"year": year, "term": term, "campus": campus}
    )
    response.raise_for_status()
    return set(response.json())

def watch_sections(indices, interval=60):
  
    print(f"Watching {len(indices)} sections... checking every {interval} seconds.")

    while True:
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

# Example usage:

watch_sections(SECTIONS_TO_WATCH)



