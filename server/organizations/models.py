from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime
from server.common import PyObjectId  # from our earlier step

class OrgBase(BaseModel):
    name: str
    

class OrgCreate(OrgBase):
    pass

class OrgInDB(OrgBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
