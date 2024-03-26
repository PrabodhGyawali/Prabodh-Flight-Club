from data_manager import DataManager
from notification_manager import NotificationManager
from flight_search import FlightSearch
from flight_data import FlightData

DEPARTURE_CODE = "LON"
data_manager = DataManager()
sheet_data = data_manager.get_sheet_data()

if sheet_data["prices"][0]["iataCode"] == "":
    flight_search = FlightSearch()
    data_manager.edit_iatacode(flight_search)

# If the price is lower than the lowest price listed in Google Sheet, send an SMS to your with the Twilio API.

for row in sheet_data["prices"]:
    flightSearcher = FlightSearch()
    flight_data = flightSearcher.get_flight_data(code=flightSearcher.get_destination_code(row["city"]),
                                                 departure_code=DEPARTURE_CODE)
    print(flight_data)
    # if flight_data is not None:
    #     if flight_data.price <= row["lowestPrice"]:
    #         flight_data.print_flight_data()
    #         notification_manager = NotificationManager(flight_data.flight_message())
    #         emails = DataManager.get_customer_emails()
    #         notification_manager.send_emails(emails)









