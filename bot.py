import requests
from bs4 import BeautifulSoup
import time
import os
# =========================
# Telegram Data
# =========================

BOT_TOKEN = os.getenv("8762856676:AAF5egGKU9crdsZcd_CzgWoeZcfEjlpjFL8")
CHAT_ID = os.getenv("1196795944")

# =========================
# ntfy Notification
# =========================

TOPIC = "haidy_jobs"

# =========================

URL = "https://freelanceyard.com/en/jobs"

sent_jobs = set()

# =========================
# Telegram Function
# =========================

def send_telegram(message):

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(telegram_url, data=data)
send_telegram("🔥 Telegram Test")
# =========================
# Phone Notification Function
# =========================

def send_phone_notification(message):

    requests.post(
        f"https://ntfy.sh/{TOPIC}",
        data=message.encode("utf-8")
    )
send_phone_notification("🔥 Test Notification")
# =========================
# Check Jobs
# =========================

def check_jobs():

    response = requests.get(URL)

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = soup.find_all("a", href=True)

    for job in jobs:

        title = job.get_text(strip=True)
        link = job["href"]

        if "/job/" in link and title:

            full_link = "https://freelanceyard.com" + link

            if full_link not in sent_jobs:

                sent_jobs.add(full_link)

                message = f"""
🚀 New Job Posted!

📌 {title}

🔗 {full_link}
"""

                # Send Telegram
                send_telegram(message)

                # Send Phone Notification
                send_phone_notification(message)

                print("New Job Sent:", title)

# =========================

try:
    check_jobs()

except Exception as e:
    print("Error:", e)