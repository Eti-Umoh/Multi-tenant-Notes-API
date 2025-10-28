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
                                            "Email": email,
                                            "Name": "New User"
                                    }
                            ],
                            "Subject": "Account Created",
                            "TextPart": f"Hello, welcome. Use the following credentials to login:\
                                email address:{email}, password:{password}",
                            "HTMLPart": f"""<h3>Hello, welcome.</h3><br/><h4>Use the following credentials below to login:</h4>\
                                <br/><h4>email address:{email}</h4><br/><h4>password:{password}</h4>"""
                        }
                ]
        }
        result = mailjet.send.create(data=data)
        return success_response(message="Email sent successfully!",
                                body=result.json(), status=result.status_code)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {e}")
