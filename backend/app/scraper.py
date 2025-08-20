import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from . import models, crud
from datetime import datetime
import time

BASE_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

def scrape_varzesh3(db: Session):
    url = "https://www.varzesh3.com"
    
    try:
        headers = {
            'User-Agent': BASE_USER_AGENT
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        news_items = []
        
        news_list = soup.select_one('.news-main-list.scrollable-box ul')
        if not news_list:
            print("News list not found")
            return []
        
        news_elements = news_list.select('li[data-newsid]')
        
        for element in news_elements[:10]: 
            try:
                news_id = element.get('data-newsid')
                if not news_id:
                    continue
                
                # Check if the news item already exists
                existing_news = crud.get_news_by_id(db, news_id)
                if existing_news:
                    continue
                
                link_element = element.find('a')
                if not link_element:
                    continue
                    
                title = link_element.get_text().strip()
                link = link_element.get('href')
                
                if not link.startswith('http'):
                    link = url + link
                
                content = scrape_news_content(link)
                
                news_item = models.News(
                    news_id=news_id,
                    title=title,
                    content=content,
                    link=link,
                    published_date=datetime.now()
                )
                news_items.append(news_item)
                
                time.sleep(0.5) 
                
            except Exception as e:
                print(f"Error processing news item {news_id}: {e}")
                continue
        
        return news_items
        
    except Exception as e:
        print(f"Error scraping Varzesh3: {e}")
        return []

def scrape_news_content(news_url):
    try:
        headers = {
            'User-Agent': BASE_USER_AGENT
        }
        response = requests.get(news_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        content_element = soup.select_one('.news-content, .content, .news-text, article')
        content = content_element.get_text().strip() if content_element else "محتوای خبر در دسترس نیست"
        
        return content
        
    except Exception as e:
        print(f"Error scraping news content {news_url}: {e}")
        return "خطا در دریافت محتوای خبر"