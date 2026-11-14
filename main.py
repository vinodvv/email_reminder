import csv
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from datetime import datetime
from pathlib import Path


def load_credentials():
    if not load_dotenv():
        raise FileNotFoundError(".env file not found.")

    email_address = os.getenv("EMAIL_ADDRESS")
    if not email_address:
        raise ValueError("EMAIL_ADDRESS is missing in .env file.")
    email_password = os.getenv("EMAIL_PASSWORD")
    if not email_password:
        raise ValueError("EMAIL_PASSWORD is missing in .env file.")

    return email_address, email_password


def load_reminders(filepath="reminders.csv"):
    with open(filepath, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        reminders = list(reader)
    return reminders


def login_to_email(email_address, email_password):
    smtp = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
    try:
        smtp.starttls()
        smtp.login(email_address, email_password)
    except Exception:
        smtp.close()
        raise
    return smtp


def create_email(r):
    msg = EmailMessage()
    msg['Subject'] = "⏰ Your Reminder for Today"
    msg['From'] = "Vinod V V"
    msg["To"] = r['email']
    msg.set_content(f"Message: {r['message']}\n"
                    f"Date: {r['date']}\n"
                    f"Time: {r['time']}")
    return msg


def save_reminders(remaining, filepath="reminders.csv"):
    filepath = Path(filepath)
    tmp_path = filepath.with_suffix(".tmp")
    with open(tmp_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file,
                                fieldnames=["date", "time", "email", "message"])
        writer.writeheader()
        writer.writerows(remaining)
    os.replace(tmp_path, filepath)


reminders = load_reminders()
today = datetime.now().strftime("%Y-%m-%d")
remaining = []
email_address, email_password = load_credentials()
smtp = login_to_email(email_address, email_password)

for r in reminders:
    if r['date'] == today:
        msg = create_email(r)
        smtp.send_message(msg)
    else:
        remaining.append(r)

save_reminders(remaining)

print(f"Emails send successfully!")