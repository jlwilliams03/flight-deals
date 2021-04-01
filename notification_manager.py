# This class is responsible for sending notifications with the deal flight details.
# Notifications via Twilio:  https://twilio.com/docs/sms
import os
from twilio.rest import Client

DO_NOT_SMS = True  # If True suppress sending an SMS message

# Account Sid and Auth Token from twilio.com/console
# set as environment variables. See http://twil.io/secure
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

class NotificationManager:
    def __init__(self):

        self.msg_from = '+13058512291'
        self.msg_to = '+15551234567'
        self.client = Client(account_sid, auth_token)

    def send_notification(self, price, from_city, from_code, to_city, to_code, leave_date,
                          return_date):
        msg_body = f"✈AIRFARE ALERT\nFare: ${price}\n{from_city} ({from_code}) ➔  {to_city} ({to_code})\nLeaving {leave_date}\nReturning {return_date}"
        print(msg_body)
        if not DO_NOT_SMS:
            message = self.client.messages.create(
                body=msg_body,
                from_=self.msg_from,
                to=self.msg_to
            )
