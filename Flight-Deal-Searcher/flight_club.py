
import requests
import os

def get_user_info():
    user_first_name = input("Welcome to Roy's Flight Club.\nWe find the best flight deals and email you.\nWhat is your first name?\n")
    user_last_name = input("What is your last name?\n")
    user_email = input("What is your email?\n")
    confirm_user_email = input("Type your email again.\n")
    if user_email != confirm_user_email:
        print("You seem to have mistyped your email. Please start again")
        get_user_info()
    else:
        print("You're in the club!")
        return {
            "firstName": user_first_name,
            "lastName": user_last_name,
            "email": user_email
        }
user_info = get_user_info()
SHEETY_API = os.getenv("SHEETY_API")
SHEETY_AUTH = os.getenv("SHEETY_AUTH")
SHEETY_PATH = f"https://api.sheety.co/{SHEETY_API}/flightDeals/users"
sheety_headers = {
    "Authorization": f"Basic {SHEETY_AUTH}"
}

response = requests.post(url = SHEETY_PATH, headers = sheety_headers, json = {"user": user_info})
response.raise_for_status()