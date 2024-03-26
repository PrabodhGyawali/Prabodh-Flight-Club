import requests

import data_manager
from data_manager import DataManager
from notification_manager import NotificationManager
import os
import random


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


SHEETY_TOKEN = "###################"
# Users
PUT_ENDPOINT = f"https://api.sheety.co/edf5d78b6078ccf41042b0ae97ca4812/flightDealsPrab/users/"
GET_ENDPOINT = "https://api.sheety.co/edf5d78b6078ccf41042b0ae97ca4812/flightDealsPrab/users"
POST_ENDPOINT = "https://api.sheety.co/edf5d78b6078ccf41042b0ae97ca4812/flightDealsPrab/users"
# Settings
SETTING_POST_ENDPOINT = "https://api.sheety.co/edf5d78b6078ccf41042b0ae97ca4812/flightDealsPrab/settings"
SETTING_PUT_ENDPOINT = f"https://api.sheety.co/edf5d78b6078ccf41042b0ae97ca4812/flightDealsPrab/settings/"
SETTING_DEL_ENDPOINT = f"https://api.sheety.co/edf5d78b6078ccf41042b0ae97ca4812/flightDealsPrab/settings/"

header = {"Authorization": f"Bearer {SHEETY_TOKEN}"}

# Common Functions


def post_user_details(first_name, last_name, email):
    row_json = {
        "user": {
            "firstName": first_name,
            "lastName": last_name,
            "email": email
        }
    }
    requests.post(url=POST_ENDPOINT, json=row_json, headers=header)


def edit_user_details(email, data_name, edited_value, mode="cred"):
    if mode == "cred":
        user_data = DataManager.get_customer_data()
        for i in range(len(DataManager.get_customer_emails())):
            if email == user_data['users'][i]['email']:
                row_id = user_data['users'][i]['id']
                edit_json = {
                    'user': {data_name: edited_value}
                }
                response = requests.put(url=f"{PUT_ENDPOINT}/{row_id}", json=edit_json, headers=header)
                # print(response.text)
    elif mode == "settings":
        user_data = DataManager.get_customer_data(mode="settings")
        for i in range(len(DataManager.get_customer_emails())):
            if email == user_data['settings'][i]['email']:
                row_id = user_data['settings'][i]['id']
                edit_json = {
                    'setting': {data_name: edited_value}
                }
                response = requests.put(url=f"{SETTING_PUT_ENDPOINT}/{row_id}", json=edit_json, headers=header)
                print(response.text)


def verify_data(data_name, mode=0):
    if mode == 0:
        return input(f"What is your {data_name}?\n")
    else:
        input1 = input(f"What is your {data_name}?\n")
        input2 = input(f"Type your {data_name} again:\n")
        while input1 != input2:
            print(f"The {data_name}s don't match! \n")
            input1 = input(f"What is your {data_name}?\n")
            input2 = input(f"Type your {data_name} again:\n")
        return input1

# Account-related functions


def sign_up():
    first_name = verify_data("first name")
    last_name = verify_data("last name")
    email = verify_data("email address")
    if email in DataManager.get_customer_emails():
        print("This email address has already signed up.")
        return email, False
    else:
        try:
            post_user_details(first_name=first_name,
                              last_name=last_name,
                              email=email)
        except Exception:
            print("Sorry an unexpected error occurred. For further information please contact prabodh.gyawali@gmail.com")
        else:
            os.system('cls')
            post_user_settings(email)
            print("Success! Your email has been added to the mailing list.")
            return email, True


def create_password(email):
    password = verify_data("password", mode=1)
    try:
        edit_user_details(email=email, data_name="password", edited_value=password)
    except Exception:
        print("Sorry an unexpected error occurred. For further information please contact prabodh.gyawali@gmail.com")


def login():
    # Ask credentials to log in
    cls()
    print("Log in")
    print("-------------------------")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    user_data = DataManager.get_customer_data()
    customer_emails = DataManager.get_customer_emails()
    if email in customer_emails:
        # Check password
        real_password = user_data['users'][customer_emails.index(email)]['password']
        if real_password == password:
            print("Login successful.")
            return True, email
        else:
            print("Wrong password!")
            return False, email
    else:
        print("Wrong email")
        return False, email


def forgot_password():
    # Send randomly generated OTP code to email
    cls()
    print("Reset password")
    print("-------------------------")
    email = input("Enter your email: ")
    # Check if email found
    if email in DataManager.get_customer_emails():

        def send_otp():
            random_code = ""
            for i in range(4):
                random_code += str(random.randint(0, 9))
            try:
                NotificationManager.send_ui_email(email, random_code)
            except Exception: # Email doesn't exist exception, or isn't @gmail.com
                pass
            finally:
                return random_code
        if send_otp() == input("Enter the OTP code sent to your email: "):
            create_password(email)
            print("Password successfully reset.")
        else:
            print("OTP code does not match.")

    else:
        print("Email not found!")


def account_services(email, option):
    if option == "A":
        user_name = "egusername"
        new_user_name = input("Enter your new username: ")
        if new_user_name != user_name:
            print(f"Username successfully changed to {user_name}")
        else:
            print("Same username entered please try again. ")
# Flight-settings-related functions
def post_user_settings(email):
    settings = {
        "setting": {
            "email": email,
            "departureCode": "LON",
            "destinationCities": "Paris, Berlin, Tokyo, Sydney, New York",
            "minimumPrices": "54, 42, 485, 551, 95, 414, 240, 260, 378, 501",
            "pause": "F",
        }
    }
    response = requests.post(url=SETTING_POST_ENDPOINT, headers=header, json=settings)
    # print(response.text)


def flight_services(email, option):
    SETTINGS_PUT_API = f"https://api.sheety.co/edf5d78b6078ccf41042b0ae97ca4812/flightDealsPrab/settings/"
    SETTINGS_POST_API = "https://api.sheety.co/edf5d78b6078ccf41042b0ae97ca4812/flightDealsPrab/settings"
    SETTINGS_GET_API = "https://api.sheety.co/edf5d78b6078ccf41042b0ae97ca4812/flightDealsPrab/settings"
    user_settings = DataManager.get_customer_data(mode="settings")
    print(user_settings)
    i = 0
    if i == 0:
        return 1

    for i in range(len(user_settings['settings'])):
        if email == user_settings['settings'][i]['email']:
            user_setting = user_settings['settings'][i]
    if option == "A":
        new_code = input("Input a valid 3-letter Airport code: ")
        # TODO: Check whether Iata code is valid
        edit_user_details(email, "departureCode", new_code, mode="settings")
    elif option == "B":
        city = input("Enter a city name: ")
        # TODO: Ensure it is valid city name:
        input_price = input("Enter a minimum price for a round trip: ")
        while not input_price.isnumeric():
            print("Invalid input, please enter a number between 1 and 10000")
            input_price = input("Enter a minimum price for a round trip: ")
        price = int(input_price)
        while 0 > price or price > 10000:
            print("Invalid input, please enter a number between 1 and 10000")
            price = input("Enter a minimum price for a round trip: ")
        city_list_string = user_setting['destinationCities']
        city_list_string += f", {city}"
        edit_user_details(email, "destinationCities", edited_value=city_list_string, mode="settings")
        price_list_string = user_setting['minimumPrices']
        price_list_string += f", {price}"
        print(price_list_string)
        edit_user_details(email, "minimumPrices", edited_value=price_list_string, mode="settings")

    elif option == "C":
        # Edit a destination city's lowest flight price
        # Print the list of Destination cities to allow user to choose
        pass
    elif option == "D":
        # Delete a destination city
        city_list = [x.strip() for x in user_setting['destinationCities'].split(',')]
        price_list = [x.strip() for x in user_setting['minimumPrices'].split(',')]
        service_message = "Choose the city you'd like to remove from the list below: \n"
        for i in range(len(city_list)):
            service_message += f"{city_list[i]}: ${price_list[i]}\n"
        print(service_message)
        city = input("City to delete from mailing list: ")
        while city not in city_list:
            print("Invalid city choice, make sure the city is within the list shown above.")
            city = input("City to delete from mailing list: ")

        del price_list[(city_list.index(city))]
        city_list.remove(city)

        city_list_string = ", ".join(city_list)
        price_list_string = ", ".join(price_list)
        edit_user_details(email, "destinationCities", edited_value=city_list_string, mode="settings")
        edit_user_details(email, "minimumPrices", edited_value=price_list_string, mode="settings")
    elif option == "E":
        # Archive a destination city
        city_list = [x.strip() for x in user_setting['destinationCities'].split(',')]
        price_list = [x.strip() for x in str(user_setting['minimumPrices']).split(',')]
        service_message = "Choose the city you'd like to archive from the list below: \n"
        for i in range(len(city_list)):
            service_message += f"{city_list[i]}: ${price_list[i]}\n"
        print(service_message)
        city = input("City to archive from mailing list: ")
        while city not in city_list:
            print("Invalid city choice, make sure the city is within the list shown above.")
            city = input("City to archive from mailing list: ")


        # Add to archive city list in DB
        archived_cities = [x.strip() for x in user_setting['archivedCities'].split(',')]
        archived_cities.append(city)
        edit_user_details(email, "archivedCities", edited_value=", ".join(archived_cities), mode="settings")

        # Add to archive price list
        archived_prices = [x.strip() for x in str(user_setting['archivedPrices']).split(',')]
        archived_prices.append(price_list[(city_list.index(city))])
        edit_user_details(email, "archivedPrices", edited_value=", ".join(archived_prices), mode="settings")

        # Delete from price list in DB
        del price_list[(city_list.index(city))]
        edit_user_details(email, "minimumPrices", edited_value=", ".join(price_list), mode="settings")

        # Delete from city list in DB
        city_list.remove(city)
        edit_user_details(email, "destinationCities", edited_value=", ".join(city_list), mode="settings")

    elif option == "F":
        if user_setting['archivedCities'] == "":
            print("There are no archived cities. This function only works if there is one or more archived city")
        else:
            # print the archived cities etc
            pass
    elif option == "G":
        # Print active Destination city: Minimum Price
            pass


