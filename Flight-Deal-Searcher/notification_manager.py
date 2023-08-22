from dotenv import load_dotenv
import os, smtplib, requests
from twilio.rest import Client

load_dotenv()

TWILIO_API = os.getenv("TWILIO_API")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
MY_NUMBER = os.getenv("MY_NUMBER")
MY_EMAIL = os.getenv("MY_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SHEETY_API = os.getenv("SHEETY_API")
SHEETY_AUTH = os.getenv("SHEETY_AUTH")
SHEETY_PATH = f"https://api.sheety.co/{SHEETY_API}/flightDeals/users"
sheety_headers = {
            "Authorization": f"Basic {SHEETY_AUTH}"
        }

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_API)
        self.connection = smtplib.SMTP("smtp.gmail.com", port = 587)
        
    def send_message(self, message):
        print("txt", message)
        message = self.client.messages.create(
            body = message,
            from_ = TWILIO_NUMBER,
            to = MY_NUMBER
        )
        print(message.sid)
        
    def send_emails(self, message):
        print("email", message)
        self.connection.starttls()
        self.connection.login(user = MY_EMAIL, password = EMAIL_PASSWORD)
        response = requests.get(url = SHEETY_PATH, headers = sheety_headers)
        response.raise_for_status()
        data = response.json()['users']
        for email in data:
            self.connection.sendmail(
                from_addr = MY_EMAIL,
                to_addrs = email['email'],
                msg = message
            )
        print("Emails sent!")
        