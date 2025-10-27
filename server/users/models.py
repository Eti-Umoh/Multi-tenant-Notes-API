# server/models/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from bson import ObjectId
from datetime import datetime, timezone
from server.common import PyObjectId  # from our earlier step


Role = Literal["reader", "writer", "admin"]

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email_address: EmailStr
    password: str
    role: Role

class UserOut(BaseModel):
    id: PyObjectId = Field(alias="_id")
    first_name: str
    last_name: str
    email_address: EmailStr
    role: Role
    organization_id: PyObjectId
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    class Config:
        json_encoders = {PyObjectId: str}
        populate_by_name = True
