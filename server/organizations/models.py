from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional
from datetime import datetime, timezone
from server.common import PyObjectId  # from our earlier step

class OrganizationCreate(BaseModel):
    name: str
    description: Optional[str] = None
    admin_email: EmailStr


class OrganizationOut(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
