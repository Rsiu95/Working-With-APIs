import requests
from dotenv import load_dotenv
import os

load_dotenv()

SHEETY_API = os.getenv("SHEETY_API")
SHEETY_AUTH = os.getenv("SHEETY_AUTH")
SHEETY_PATH = f"https://api.sheety.co/{SHEETY_API}/flightDeals/prices"
sheety_headers = {
    "Authorization": f"Basic {SHEETY_AUTH}"
}

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.response = requests.get(url = SHEETY_PATH, headers = sheety_headers)
        self.response.raise_for_status()
        self.prices = self.response.json()
        
    def update_sheet(self, prices, id):
        self.response = requests.put(url = SHEETY_PATH + f"/{id}", headers = sheety_headers, json = prices)
        self.response.raise_for_status()
