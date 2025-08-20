import time
import threading
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from .database import SessionLocal, engine
from . import models, schemas, crud, scraper

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Varzesh3 News Reader", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def periodic_scrape():
    while True:
        try:
            db = SessionLocal()
            new_news = scraper.scrape_varzesh3(db)
            for news in new_news:
                crud.create_news(db, news)
            db.close()
            print(f"Periodic scrape completed. Added {len(new_news)} new news items.")
        except Exception as e:
            print(f"Periodic scrape error: {e}")
        time.sleep(60) # every minute

# Creating thread for periodic scraper (60 seconds interval)
scrape_thread = threading.Thread(target=periodic_scrape, daemon=True)
scrape_thread.start()


# FastAPI endpoints:
@app.get("/")
def read_root():
    return {"message": "Varzesh3 News Reader API"}

@app.get("/news/", response_model=List[schemas.News])
def read_news(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    news = crud.get_news(db, skip=skip, limit=limit)
    return news

@app.get("/news/search/", response_model=List[schemas.News])
def search_news(q: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if not q:
        return crud.get_news(db, skip=skip, limit=limit)
    news = crud.search_news(db, query=q, skip=skip, limit=limit)
    return news

@app.post("/news/", response_model=schemas.News)
def create_news(news: schemas.NewsCreate, db: Session = Depends(get_db)):
    db_news = crud.get_news_by_link(db, link=news.link)
    if db_news:
        raise HTTPException(status_code=400, detail="News already exists")
    return crud.create_news(db, news)

    