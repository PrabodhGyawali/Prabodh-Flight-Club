import requests
from sqlalchemy import Table

class DataManager:
    # This class is responsible for talking to Sheety API
    def __init__(self):
        self.header = {"Authorization": f"Bearer {SHEETY_TOKEN}"}

    def get_sheet_data(self):
        # read file to get number of lines
        response = requests.get(url=GET_PRICES_ENDPOINT, headers=self.header)
        print(response.text)
        data = response.json()
        return data

    def get_column_list(self, column_name):
        data = self.get_sheet_data()
        column_list = [x[column_name] for x in data["prices"]]
        return column_list

    def edit_iatacode(self, flight_search_object):
        data = self.get_sheet_data()
        # edit IATA code
        i = 0
        city_list = self.get_column_list("city")
        for row in data['prices']:
            row_json_edit = {
                "price": {
                        "iataCode": flight_search_object.get_destination_code(city_list[i]),
                    }
            }
            put_url = f"https://api.sheety.co/edf5d78b6078ccf41042b0ae97ca4812/flightDealsPrab/prices/{row['id']}"
            requests.put(url=put_url, json=row_json_edit, headers=self.header)
            i += 1

    @staticmethod
    def get_customer_emails():
        response = requests.get(url=GET_USERS_ENDPOINT, headers={"Authorization": f"Bearer {SHEETY_TOKEN}"})
        data = response.json()
        return [x["email"] for x in data["users"]]

    @staticmethod
    def get_customer_data(mode="cred"):
        if mode == "cred":
            response = requests.get(url=GET_USERS_ENDPOINT, headers={"Authorization": f"Bearer {SHEETY_TOKEN}"})
            data = response.json()
            return data
        elif mode == "settings":
            response = requests.get(url=SETTING_GET_ENDPOINT, headers={"Authorization": f"Bearer {SHEETY_TOKEN}"})
            data = response.json()
            return data

