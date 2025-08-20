import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from . import models, crud
from datetime import datetime
import time
import re
import jdatetime
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
                
                news_details = scrape_news_content(link)
                content = news_details[0]
                published_date = news_details[1]
                image_url = news_details[2]

                news_item = models.News(
                    news_id=news_id,
                    title=title,
                    content=content,
                    link=link,
                    published_date=published_date,
                    image_url=image_url
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(news_url, headers=headers, timeout=10)
        response.raise_for_status()

        page_content = response.text
        
        image_url = ""
        
        pattern = r'https://news-cdn\.varzesh3\.com/pictures/[\w/.-]+\.(?:webp|jpg|jpeg|png)'
        matches = re.findall(pattern, page_content)
        
        if matches:
            image_url = matches[0]
            print(f"Image URL found: {image_url}")

        soup = BeautifulSoup(response.content, 'html.parser')
        
        content_element = soup.select_one('.news-content, .content, .news-text, article')
        content = content_element.get_text().strip() if content_element else "محتوای خبر در دسترس نیست"
        
        date_text = None
        
        all_spans = soup.find_all('span')
        
        for i, span in enumerate(all_spans):
            text = span.get_text().strip()
            if "کد:" in text:
                if i + 1 < len(all_spans):
                    next_span = all_spans[i + 1]
                    date_text = next_span.get_text().strip()
                    break
        
        if not date_text:
            for span in all_spans:
                text = span.get_text().strip()
                if any(month in text for month in ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 
                                                 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']):
                    date_text = text
                    break
        published_date = parse_persian_date(date_text) if date_text else datetime.now()
        
        return content, published_date, image_url
        
    except Exception as e:
        print(f"Error scraping news content {news_url}: {e}")
        return "خطا در دریافت محتوای خبر", datetime.now(), ""
    
def parse_persian_date(persian_date_str):
    try:
        pattern = r'(\d{1,2})\s+(\S+)\s+(\d{4})\s+ساعت\s+(\d{1,2}):(\d{2})'
        match = re.search(pattern, persian_date_str)
        
        if not match:
            return datetime.now()
        
        day = int(match.group(1))
        month_name = match.group(2)
        year = int(match.group(3))
        hour = int(match.group(4))
        minute = int(match.group(5))
        
        month_map = {
            'فروردین': 1, 'اردیبهشت': 2, 'خرداد': 3,
            'تیر': 4, 'مرداد': 5, 'شهریور': 6,
            'مهر': 7, 'آبان': 8, 'آذر': 9,
            'دی': 10, 'بهمن': 11, 'اسفند': 12
        }
        
        month = month_map.get(month_name, 1)
        
        jalali_date = jdatetime.date(year, month, day)
        gregorian_date = jalali_date.togregorian()
        
        return datetime(
            gregorian_date.year, 
            gregorian_date.month, 
            gregorian_date.day,
            hour, minute
        )
        
    except Exception as e:
        print(f"Error parsing Persian date '{persian_date_str}': {e}")
        return datetime.now()