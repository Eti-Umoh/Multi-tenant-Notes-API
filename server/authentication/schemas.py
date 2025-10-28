from pydantic import BaseModel

class LoginUser(BaseModel):
    email_address: str
    password: str
