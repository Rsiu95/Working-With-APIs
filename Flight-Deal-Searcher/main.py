#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager
import datetime as dt
from dotenv import load_dotenv

load_dotenv()

sheet_data = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

DEPARTURE_CITY_CODE = "MEL"

for data in sheet_data.prices['prices']:
    city = flight_search.get_destination_code(data['city'])
    data['iataCode'] = city

for data in sheet_data.prices['prices']:
    id = data['id']
    new_data = {
        "price": {
            "iataCode": data["iataCode"]
        }
    }
    sheet_data.update_sheet(new_data, id)

tomorrow = dt.datetime.now() + dt.timedelta(days = 1)
departure_range = tomorrow + dt.timedelta(days = 182.5)

for code in sheet_data.prices['prices']:
    flight_search_data = flight_search.search_flights(DEPARTURE_CITY_CODE, code["iataCode"], tomorrow, departure_range)
    if flight_search_data is None:
        continue
    
    if flight_search_data.price < code['lowestPrice']:
        message = f"Low price alert! only ${flight_search_data.price} to fly from {flight_search_data.departure_city}-{flight_search_data.departure_airport_code} to {flight_search_data.destination_city}-{flight_search_data.destination_airport_code}, from {flight_search_data.departure_date} to {flight_search_data.return_date}"
        
        if flight_search_data.stop_overs > 0:
            message += f"\n Flight has {flight_search_data.stop_overs} stop over, via {flight_search_data.via_city}"
        
        notification_manager.send_message(message)
        notification_manager.send_emails(message)

        

