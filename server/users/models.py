# server/models/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from bson import ObjectId
from datetime import datetime, timezone
from server.common import PyObjectId  # from our earlier step

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email_address: EmailStr
    role: Literal["admin", "writer", "reader"] = "admin"
    organization_id: PyObjectId

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
