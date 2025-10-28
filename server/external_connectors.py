from fastapi import HTTPException
from mailjet_rest import Client
from server.config import settings
from server.main_utils import success_response

api_key = settings.MAILJET_API_KEY
api_secret = settings.MAILJET_SECRET_KEY
sender = settings.SENDER_EMAIL

async def send_email(email, password):
    try:
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
        'Messages': [
                        {
                            "From": {
                                    "Email": sender,
                                    "Name": "Notes API"
                            },
                            "To": [
                                    {
                                            "Email": "$RECIPIENT_EMAIL",
                                            "Name": "You"
                                    }
                            ],
                            "Subject": "Account Created",
                            "TextPart": "Hello, welcome",
                            "HTMLPart": f"""<h4>Use the following credentials below to login:</h4>\
                                <br/><h3>email address:{email}</h3><br/><h3>password:{password}</h3>"""
                        }
                ]
        }
        result = mailjet.send.create(data=data)
        return success_response(message="Email sent successfully!",
                                body=result.json(), status=result.status_code)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {e}")
