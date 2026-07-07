from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class NotificationBase(BaseModel):
    title: str
    message: str

class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    claim_id: Optional[int] = None
    title: str
    message: str
    is_read: bool
    created_at: datetime

class NotificationUnreadCountResponse(BaseModel):
    unread_count: int
