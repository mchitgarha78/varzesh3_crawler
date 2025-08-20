from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas

def get_news(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.News).filter(models.News.is_active == True).order_by(models.News.published_date.desc()).offset(skip).limit(limit).all()

def get_news_by_id(db: Session, news_id: str):
    return db.query(models.News).filter(models.News.news_id == news_id).first()

def create_news(db: Session, news: schemas.NewsCreate):
    db_news = models.News(
        news_id=news.news_id,
        title=news.title,
        content=news.content,
        link=news.link,
        published_date=news.published_date,
        category=news.category
    )
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

def search_news(db: Session, query: str, skip: int = 0, limit: int = 100):
    return db.query(models.News).filter(
        models.News.is_active == True,
        or_(
            models.News.title.ilike(f"%{query}%"),
            models.News.content.ilike(f"%{query}%")
        )
    ).order_by(models.News.published_date.desc()).offset(skip).limit(limit).all()