class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, price, departure_airport_code, departure_city, destination_airport_code, destination_city, \
                return_date, departure_date, stop_overs=0, via_city=""):
        self.price = price
        self.departure_airport_code = departure_airport_code
        self.departure_city = departure_city
        self.destination_airport_code = destination_airport_code
        self.destination_city = destination_city
        self.return_date = return_date
        self.departure_date = departure_date
        self.stop_overs = stop_overs
        self.via_city = via_city