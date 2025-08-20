from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NewsBase(BaseModel):
    news_id: str
    title: str
    content: Optional[str] = None
    link: str
    image_url: Optional[str] = None
    published_date: Optional[datetime] = None
    category: Optional[str] = None

class NewsCreate(NewsBase):
    pass

class News(NewsBase):
    id: int
    created_at: datetime
    is_active: bool

    class Config:
        orm_mode = True