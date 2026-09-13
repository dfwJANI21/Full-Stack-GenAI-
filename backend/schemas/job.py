from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class StoryJobBase(BaseModel):
    theme: str

class StoryJobResponse(BaseModel):
    job_id: str
    status: str
    created_at: datetime
    story_id: Optional[int] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None

    class config:
        from_attributes = True

class StoryJobCreate(StoryJobBase):
    pass

