from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from datetime import datetime, timezone
from server.common import PyObjectId  # from our earlier step

class OrganizationBase(BaseModel):
    name: str
    description: Optional[str] = None
    

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationOut(OrganizationBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
