# server/models/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from datetime import datetime, timezone
from server.common import PyObjectId


Role = Literal["reader", "writer", "admin"]

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email_address: EmailStr
    role: Role

class UserOut(BaseModel):
    id: PyObjectId = Field(alias="_id")
    first_name: str
    last_name: str
    email_address: EmailStr
    role: Role
    password: str
    organization_id: PyObjectId
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    class Config:
        json_encoders = {PyObjectId: str}
        populate_by_name = True
