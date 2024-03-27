import twilio.rest
import smtplib

# Client API
account_sid = "############"
auth_token = "#############"

# Email User details
username = "#########@gmail.com"
password = "##############"

# This class is responsible for sending notifications
class NotificationManager:
    # Create messaging function:
        # Message append
        # Message clear
        # Message send

    # SMS notification
    def __init__(self, message):
        self.message = message

    def send_sms(self):
        client = twilio.rest.Client(account_sid, auth_token)
        message = client.messages \
            .create(
                    body=self.message,
                    shorten_urls="true",
                    from_="+############",
                    to="+##########")

    # Email notification: as its free
    def send_emails(self, emails):
        for email in emails:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                 connection.starttls()
                 connection.login(user=username, password=password)
                 connection.sendmail(from_addr=username,
                                     to_addrs=email,
                                     msg=f"Subject:Prabodh's Flight Club!\n\n{self.message}".encode("utf-8"))

    @staticmethod
    def send_ui_email(email, message):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=username, password=password)
            connection.sendmail(from_addr=username,
                                to_addrs=email,
                                msg=f"Subject:Forgot Flight Club password\n\nYour OTP code is: {message}".encode("utf-8"))
