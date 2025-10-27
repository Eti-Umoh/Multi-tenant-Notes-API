from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime
from server.models.common import PyObjectId  # from our earlier step

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email_address: EmailStr
    phone_number: str
    gender: Optional[str] = None
    user_type: Optional[str] = "investor"
    referral_code: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
