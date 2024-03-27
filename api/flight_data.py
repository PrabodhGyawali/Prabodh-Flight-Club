
class FlightData:
    # This class is responsible for structuring the flight data.
    # TODO: Learn how to use an API to create shorter links: twilio or an external api

    def __init__(self, price, origin_city, origin_airport, destination_city, destination_airport, out_date, return_date, link, stop_overs=0, via_city=""):
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stop_overs = stop_overs
        self.via_city = via_city
        self.link = link

    def print_flight_data(self):
        print(f"{self.destination_city}: £{self.price}")
        if self.stop_overs == 1:
            print(f"Flight has 1 stop over, via {self.via_city}")

    # Fix this message
    def flight_message(self):
        message = f"Low price alert!:\n" \
                  f"{self.origin_city}: {self.price}\n" \
                  f"More info: {self.link}"
        return message

