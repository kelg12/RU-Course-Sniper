# Rutgers Course Sniper

This program is a small Python script that interacts with the Rutgers Schedule of Classes API and notifies the user when a desired section opens.

This project is intented for **personal use** to track open courses during registration periods.

---

## Features

- Polls the 'openSections.json' API at a configurable interval
- Checks if specified course section is open or closed
- Sends a push notification when a section opens
- Designed to be lightweight and respectful of API usage

---

## How It Works

The script periodically queries:

https://classes.rutgers.edu/soc/api/openSections.json

This endpoint returns a list of *currently open* sections by their index values.

If the target section appears in the response, it is considered open.

The script respects WebReg downtime (2:00 AM - 5:59 AM) and sleeps during this time

---

## Requirements

- Python 3.9+
- `requests`
- ntfy for push notifications
- tzdata (If running on Windows)

Install dependecies:

```bash
pip install requests python-dotenv
```
# Configuration

## Environment Variables

Sensitive credentials are stored in environment variables and are **not included** in this repository.

An example .env file can be located in the repository that includes a template to configure your ntfy topic for push notifications.

It is best to create and activate a Python virtual environment in the repository directory:

```bash
python3 -m venv venv

source venv/bin/activate
```

Once inside the virtual environment, install dependencies:

```bash
pip install -r requirements.txt
```

Now create the `.env` file in the virtual environment following the `.env.example` template

```bash
nano .env

NTFY_TOPIC=your-topic-here
```

Test the functionality of the script by running `python sniper.py` to ensure there are no errors before exiting the virtual environment

```bash
deactivate
```

# Usage

## Watch multiple sections

Watch as many sections as desired while keeping API calls consistent at once every 60 seconds.

The program checks for changes with the API once per minute, consistent with normal browser usage.

A notification is sent out when the section opens.

## How to run as background service (recommended)

The way that I am using this script (and how you should too) is letting it run 24/7 in the background on my Raspberry Pi.

The setup is fairly straight forward using the terminal.

Start by creating the service file with:

```bash
sudo nano /etc/systemd/system/ru-course-sniper.service
```

Now copy and paste the following content, replacing {user} with your local username (assuming you cloned the repository in your home directory).

```bash
[Unit]
Description=RU Course Sniper
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User={user}
WorkingDirectory=/home/{user}/RU-Course-Sniper
ExecStart=/home/{user}/RU-Course-Sniper/venv/bin/python sniper.py
Restart=always
RestartSec=30
EnvironmentFile=/home/{user}/RU-Course-Sniper/.env
Environment=PYTHONBUFFERED=1
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Now run:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ru-course-sniper
sudo systemctl start ru-course-sniper
```

Now the service will start running after boot, restart if it crashes, and continiously run in the background.

# Example Output

```less
Watching 4 sections... checking every 60 seconds.
Section 14496 is now OPEN!
```
# Disclaimer

This project is not affiliated with or endorsed by Rutgers University and is intended for personal, non-commercial use.

This project is my first attempt at using API calls with Python and is a work in progress.

Use responsibly and at your own risk.
