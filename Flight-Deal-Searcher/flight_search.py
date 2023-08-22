import requests
from dotenv import load_dotenv
from flight_data import FlightData
import os

load_dotenv()

KIWI_API = os.getenv("KIWI_API")
KIWI_QUERY = f"https://api.tequila.kiwi.com/locations/query"
KIWI_SEARCH = f"https://api.tequila.kiwi.com/v2/search"
KIWI_HEADERS = {
        "apikey": KIWI_API,
    }

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def get_destination_code(self, city):
        location_params = {
            "term": city,
            "location_types": "airport",
        }
        response = requests.get(url = KIWI_QUERY, headers = KIWI_HEADERS, params = location_params)
        response.raise_for_status()
        data = response.json()
        for id in data['locations']:
            return id['id']

    def search_flights(self, departure_airport_code, destination_airport_code, departure_date, return_date):
        search_params = {
            "fly_from": departure_airport_code,
            "fly_to": destination_airport_code,
            "date_from": departure_date.strftime("%d/%m/%Y"),
            "date_to": return_date.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "AUD"            
        }

        response = requests.get(url = KIWI_SEARCH, headers = KIWI_HEADERS, params = search_params)
        response.raise_for_status()

        try:
            data = response.json()['data'][0]
            
        except IndexError:
            print(f"No cheaper flights found for {destination_airport_code}.")
            search_params["max_stopovers"] = 1
            response = requests.get(url = KIWI_SEARCH, headers = KIWI_HEADERS, params = search_params)
            try:
                data = response.json()['data'][0]
            except IndexError:
                return None
            else:
                flight_data = FlightData(
                    price = data["price"],
                    departure_city = data["route"][0]["cityFrom"],
                    departure_airport_code = data["route"][0]["flyFrom"],
                    destination_city = data["route"][1]["cityTo"],
                    destination_airport_code = data["route"][1]["flyTo"],
                    departure_date = data["route"][0]["local_departure"].split("T")[0],
                    return_date = data["route"][2]["local_departure"].split("T")[0],
                    stop_overs = 1,
                    via_city = data["route"][0]["cityTo"]
                )
                print(f"{flight_data.destination_city}: ${flight_data.price}")
                return flight_data
        else:
            flight_data = FlightData(
                price = data["price"],
                departure_airport_code = data["flyFrom"], 
                departure_city = data["route"][0]["cityFrom"], 
                destination_airport_code = data["flyTo"], 
                destination_city = data["route"][0]["cityTo"],
                return_date = data["route"][1]["local_departure"].split("T")[0], 
                departure_date = data["route"][0]["local_departure"].split("T")[0]
            )
            print(f"{flight_data.destination_city}: ${flight_data.price}")
            return flight_data
