from fastapi import HTTPException
from mailjet_rest import Client
import os
from server.config import settings

api_key = settings.MAILJET_API_KEY
api_secret = settings.MAILJET_SECRET_KEY

async def send_email(recipient_email: str, subject: str, content):
    try:
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

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {e}")