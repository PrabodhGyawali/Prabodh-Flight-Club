import ui_backend
import os
import time

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


print("Welcome to Prabodh's Flight Club.\n\
We find the best flight deals and email it to you.")
print("----------------------------------------")
print("If you are a new user, input '0' and press enter.\n\
If you have already signed up to the newsletter input '1' and press enter.")

user_type = input("Input: ")
while user_type != '1' and user_type != '0':
    print("Invalid input: ")
    print("If you are a new user, input '0' and press enter.\n\
    If you have already signed up to the newsletter input '1' and press enter.")
    user_type = input("Input: ")

if user_type == "0":
    # Function below asks for user credentials and adds it to the excel file
    status = ui_backend.sign_up()

    # Function below aks for user if they want to create a password
    if status[1]:
        print("Do you want to create a password to change Newsletter settings.")
        # Ask for email confirmation from user
        user_option = input("Type 'y' to create a password or any other key to quit.")
        if user_option == 'y':
            ui_backend.create_password(status[0])
        print("You have successfully created your password. Rerun the program to access your account settings.")
    else:
        user_type = input("If you want to the login to your account input '1'.\n"
                          "Or press any other key to exit program.\n")

if user_type == '1':
    # Ask credentials to log in
    login_status = ui_backend.login()

    while not login_status[0]:
        login_service = input("Press 1 to re-enter credentials.\n"
                              "Press 2 to reset password.\n"
                              "Press any other key to exit program.\n")
        if login_service == '1':
            login_status = ui_backend.login()
        elif login_service == '2':
            ui_backend.forgot_password()
        else:
            break

    if login_status[0]:
        # Access application services
        while True:
            service = input(f"Press A for editing flight settings.\n"
                            f"Press B for editing account settings.\n"
                            f"Press Q to logout and exit program.\n")
            if service == 'Q':
                break
            elif service == 'A':
                flight_service = input(f"Press A to change Departure airport code.\n"
                                       f"Press B to add a destination city and minimum price.\n"
                                       f"Press C to edit a destination city's Lowest Flight Price.\n"
                                       f"Press D to delete a destination city.\n"
                                       f"Press E to temporarily deactivate your destination city.\n"
                                       f"Press F to reactive your destination city.\n"
                                       f"Press Q to return to home.\n")
                ui_backend.flight_services(login_status[1], flight_service)
            elif service == 'B':
                account_service = input(f"Press A to change your username.\n"
                                        f"Press B for resetting password.\n"
                                        f"Type 'TRANSFER' to change email address.\n"
                                        f"Type 'PAUSE' to temporarily unsubscribe from the mailing list.\n"
                                        f"Type 'DELETE' to unsubscribe from the mailing list and clear all user data.\n"
                                        f"Press Q to return to home.\n")
                ui_backend.account_services(login_status[1], account_service)
            else:
                cls()
                print("Invalid input please try again.")
                time.sleep(1)



