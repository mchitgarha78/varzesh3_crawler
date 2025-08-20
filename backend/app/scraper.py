import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from . import models, crud
from datetime import datetime
import time
import re
import jdatetime
BASE_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'



# IMPORTANT NOTE: We can also get news list from the https://web-api.varzesh3.com/v1.0/.
# But because of the ban risk we can choose manually search and scrape. Also some data on this api is not complete.
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
        
        news_lists = soup.select('.news-main-list.scrollable-box ul')
        
        for news_list in news_lists:
            news_elements = news_list.select('li[data-newsid]')
            
            for element in news_elements[:2]:  
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
                        link = 'https://www.varzesh3.com' + link
                    
                    data_sport = element.get("data-sport")
                    if not data_sport:
                        data_sport = ""
                    category = get_category_name(data_sport)
                    
                    news_details = scrape_news_content(link)
                    content = news_details[0]
                    published_date = news_details[1]
                    image_url = news_details[2]
                    
                    news_item = models.News(
                        news_id=news_id,
                        title=title,
                        content=content,
                        link=link,
                        image_url=image_url,
                        published_date=published_date,
                        category=category
                    )
                    news_items.append(news_item)
                    
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"Error processing news item {news_id}: {e}")
                    continue
        
        news_items.sort(key=lambda x: x.published_date, reverse=True)
        
        return news_items
        
    except Exception as e:
        print(f"Error scraping Varzesh3: {e}")
        return []


def get_category_name(sport_id):
    """تبدیل آیدی ورزش به نام دسته‌بندی"""
    sport_map = {
        "1": "فوتبال",
        "3": "والیبال",
        "4": "بسکتبال",
        "16": "کشتی",
        "5": "هندبال",
        "19": "تنیس",
        "25": "اتومبیل رانی",
        "43": "اسکواش",
        "42": "اسکی",
        "27": "اسکیت",
        "21": "بدمینتون",
        "46": "بدن‌سازی",
        "23": "بسکتبال با ویلچر",
        "12": "بوکس",
        "30": "بولینگ",
        "31": "بیسبال",
        "29": "بیلیارد",
        "17": "تکواندو",
        "8": "تنیس روی میز",
        "7": "تیراندازی",
        "6": "تیراندازی با کمان",
        "45": "جوجیتسو",
        "13": "جودو",
        "14": "دو و میدانی",
        "9": "دوچرخه سواری",
        "32": "ژیمناستیک",
        "35": "سنگ‌نوردی",
        "26": "سوارکاری",
        "33": "شطرنج",
        "11": "شمشیربازی",
        "22": "شنا",
        "10": "قایقرانی",
        "20": "کاراته",
        "34": "کبدی",
        "44": "کوراش",
        "47": "گلبال",
        "36": "گلف",
        "37": "موتورسواری",
        "38": "هاکی",
        "39": "واترپلو",
        "24": "والیبال نشسته",
        "15": "وزنه برداری",
        "40": "ووشو"
    }

    if sport_id in sport_map:
        return sport_map[sport_id]
    else:
        return "سایر"

def scrape_news_content(news_url):
    try:
        headers = {
            'User-Agent': BASE_USER_AGENT
        }
        response = requests.get(news_url, headers=headers, timeout=10)
        response.raise_for_status()

        page_content = response.text
        
        image_url = ""
        
        pattern = r'https://news-cdn\.varzesh3\.com/pictures/[\w/.-]+\.(?:webp|jpg|jpeg|png)'
        matches = re.findall(pattern, page_content)
        
        if matches:
            image_url = matches[0]

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