from pydantic import BaseModel, Field
from datetime import datetime, timezone
from server.common import PyObjectId

class NoteCreate(BaseModel):
    title: str
    content: str


class NoteOut(NoteCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    content: str
    organization_id: PyObjectId
    created_by: PyObjectId  # user id
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True
        json_encoders = {PyObjectId: str}
