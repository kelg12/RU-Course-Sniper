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

This endpoint returns a list of *currently open* sections
If the target section appears in the response, it is considered open

---

## Requirements

- Python 3.9+
- 'requests'
- (Optional) Twilio account to manage SMS notifications

Install dependecies:

```bash
pip install requests twilio python-dotenv
