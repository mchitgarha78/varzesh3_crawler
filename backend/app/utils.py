from datetime import datetime
import jdatetime
import re

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