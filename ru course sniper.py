#This program will interact with the schedule of classes API to retrieve and display the status of a specific section.
import requests
import time
import os
from twilio.rest import Client

URL = "https://classes.rutgers.edu/soc/api/openSections.json"

def get_open_sections(year=2026, term=1, campus="NB"):
    response = requests.get(
        URL,
        params={"year": year, "term": term, "campus": campus}
    )
    response.raise_for_status()
    return set(response.json())

def watch_section(index, interval=60):
    key = f"{index}"
    was_open = False

    print(f"Watching {key}... checking every {interval} seconds.")

    while True:
        try:
            open_sections = get_open_sections()
            is_open = key in open_sections

            if is_open and not was_open:
                msg = f"Section {key} is now OPEN!"
                print(msg)
                send_text(msg)
                was_open = True
                break

            was_open = is_open

        except Exception as e:
            print(f"Error checking section {key}: {e}")

        time.sleep(interval)
      
def send_text(message):
    client = Client(
        os.environ["TWILIO_ACCOUNT_SID"],
        os.environ["TWILIO_AUTH_TOKEN"]
    )

    client.messages.create(
        body=message,
        from_=os.environ["TWILIO_PHONE"],
        to=os.environ["MY_PHONE"]
    )

def is_section_open(index, year=2026, term=1, campus="NB"):
    open_sections = get_open_sections(year, term, campus)
    key = f"{index}"
    return key in open_sections

# Example usage:

   #if is_section_open("14496"):
   # print("Section is OPEN")
   #else:
   # print("Section is CLOSED")
watch_section(13949)

