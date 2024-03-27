import requests
import pprint
import datetime as dt
from flight_data import FlightData
TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
TEQUILA_API_KEY = "vJ3_u6I-n2AGMJnrHGghtyrtq9gOTYOr"
header = {"apikey": TEQUILA_API_KEY}

class FlightSearch:
    # This class is responsible for talking to kiwi API
    def get_destination_code(self, city_name):
        full_api_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        query = {"term": city_name, "location_types": "airport", "active_only": "true"}
        response = requests.get(url=full_api_endpoint, headers=header, params=query)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code

    def get_flight_data(self, code, departure_code):
        full_api_endpoint = f"{TEQUILA_ENDPOINT}/v2/search"

        # Flight date manager:
        date_from = (dt.date.today() + dt.timedelta(days=1)).strftime("%d/%m/%Y")
        date_to = (dt.date.today() + dt.timedelta(days=6*30)).strftime("%d/%m/%Y")

        stop_over = 0
        search_parameters = {
            "fly_from": departure_code,
            "fly_to": code,
            "date_from": date_from,
            "date_to": date_to,
            "flight_type": "round",
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP",
            "stop_overs": stop_over,

        }
        response = requests.get(url=full_api_endpoint, headers=header, params=search_parameters)
        try:
            data = response.json()["data"][0]
        except IndexError:
            search_parameters["max_stopovers"] = 2
            response = requests.get(url=full_api_endpoint, headers=header, params=search_parameters)
            try:
                data = response.json()["data"][0]
            except IndexError:
                print(f"No flights found for {code}.")
                return None
            else:
                print(data)
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"],
                    link=data["deep_link"])
                return flight_data
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
                link=data["deep_link"])
            return flight_data






