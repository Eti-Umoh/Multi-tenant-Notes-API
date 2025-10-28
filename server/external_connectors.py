"""
Run:
"""
from mailjet_rest import Client
import os
api_key = os.environ['MJ_APIKEY_PUBLIC']
api_secret = os.environ['MJ_APIKEY_PRIVATE']
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
data = {
  'Messages': [
				{
						"From": {
								"Email": "$SENDER_EMAIL",
								"Name": "Me"
						},
						"To": [
								{
										"Email": "$RECIPIENT_EMAIL",
										"Name": "You"
								}
						],
						"Subject": "My first Mailjet Email!",
						"TextPart": "Greetings from Mailjet!",
						"HTMLPart": "<h3>Dear passenger 1, welcome to <a href=\"https://www.mailjet.com/\">Mailjet</a>!</h3><br />May the delivery force be with you!"
				}
		]
}
result = mailjet.send.create(data=data)
print result.status_code
print result.json()