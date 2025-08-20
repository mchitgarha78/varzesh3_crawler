from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class News(Base):
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True, index=True)
    news_id = Column(String, unique=True, index=True)  
    title = Column(String, index=True)
    content = Column(Text)  
    link = Column(String, unique=True, index=True)
    published_date = Column(DateTime, default=datetime.datetime.utcnow)
    category = Column(String, default="ورزشی")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)