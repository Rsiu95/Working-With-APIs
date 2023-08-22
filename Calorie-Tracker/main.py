import requests
import datetime as dt
from dotenv import load_dotenv
import os

load_dotenv()

current_date = dt.datetime.now()
date = current_date.strftime("%d/%m/%Y")
time = current_date.strftime("%H:%M:%S")

SHEETY_AUTH = os.getenv("SHEETY_AUTH")
SHEETY_API = os.getenv("SHEETY_API")
PROJECT_NAME = "myWorkouts"
SHEETNAME = "workouts"
SHEETY_PATH = f"https://api.sheety.co/{SHEETY_API}/{PROJECT_NAME}/{SHEETNAME}"

NUTRIONIX_PATH = "https://trackapi.nutritionix.com/v2/natural/exercise"
NUTRITIONIX_API = os.getenv("NUTRITIONIX_API")
NUTRITIONIX_APPID = os.getenv("NUTRITIONIX_APPID")

GENDER = "MALE"
WEIGHT_KG = "85.0"
HEIGHT_CM = "170.0"
AGE = "28"

nutritionix_headers = {
    "x-app-id": NUTRITIONIX_APPID,
    "x-app-key": NUTRITIONIX_API,
    "Content-Type": "application/json"
}

exercise_params = {
    "query":input("Tell me what exercises you did: "),
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

nutritionix_post = requests.post(url = NUTRIONIX_PATH, headers = nutritionix_headers, json = exercise_params)
nutritionix_post.raise_for_status()
response = nutritionix_post.json()

exercise_info = []
for data in response['exercises']:
    exercise_info.append({
        'date':date,
        'time':time,
        'exercise': data["name"],
        'duration': data["duration_min"],
        'calories': data["nf_calories"]
    })

print(exercise_info)

sheety_headers = {
    "Authorization": f"Basic {SHEETY_AUTH}"
}

for exercise in exercise_info:
    sheety_post = requests.post(url = SHEETY_PATH, headers = sheety_headers, json = {"workout": exercise})
    sheety_post.raise_for_status()
