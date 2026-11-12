import csv
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")


with open("reminders.csv") as file:
    reader = csv.DictReader(file)
    reminders = list(reader)


for r in reminders:
    msg = EmailMessage()
    msg['Subject'] = "⏰ Your Reminder for Today"
    msg['From'] = "Vinod V V"
    msg["To"] = r['email']
    msg.set_content(f"Message: {r['message']}\n"
                    f"Date: {r['date']}\n"
                    f"Time: {r['time']}")

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

print(f"Emails send successfully!.")