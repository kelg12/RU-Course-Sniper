# Rutgers Course Sniper

This program is a small Python script that interacts with the Rutgers Schedule of Classes API and notifies the user when a desired section opens.

This project is intented for **personal use** to track open courses during registration periods.

---

## Features

- Polls the 'openSections.json' API at a configurable interval
- Checks if specified course section is open or closed
- Sends a SMS notification when a section opens
- Designed to be lightweight and respectful of API usage

---

## How It Works

The script periodically queries:

https://classes.rutgers.edu/soc/api/openSections.json

This endpoint returns a list of *currently open* sections by their index values.

If the target section appears in the response, it is considered open.

---

## Requirements

- Python 3.9+
- 'requests'
- ntfy for push notifications

Install dependecies:

```bash
pip install requests python-dotenv
```
# Configuration

## Environment Variables

Sensitive credentials are stored in environment variables and are **not included** in this repository.

An example .env file can be located in the repository that includes a template to configure your ntfy topic for push notifications.

# Usage

## Watch multiple sections

Watch as many sections as desired while keeping API calls consistent at once every 60 seconds.

The program checks for changes with the API once per minute, consistent with normal browser usage.

A notification is sent out when the section opens.

# Example Output

```less
Watching 4 sections... checking every 60 seconds.
Section 14496 is now OPEN!
```
# Disclaimer

This project is not affiliated with or endorsed by Rutgers University and is intended for personal, non-commercial use.

Use responsibly and at your own risk.
