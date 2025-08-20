# Varzesh3 News Reader

A web application that crawls and displays news from Varzesh3.com (a popular Persian sports news website) with a modern Python backend and React frontend.

## Features

- **Automated News Crawling**: Periodically scrapes news from Varzesh3.com
- **SQLite Database**: Stores news articles with ORM (SQLAlchemy)
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **React Frontend**: Modern responsive UI with Persian (RTL) support
- **Search Functionality**: Full-text search across news titles and content
- **Real-time Updates**: Background scraping
- **Modal View**: Read full articles without leaving the site
- **Category Support**: Football, volleyball, basketball and other sports categories

## Tech Stack

### Backend
- **Python 3.13** with FastAPI
- **SQLAlchemy** ORM with SQLite
- **BeautifulSoup4** for web scraping
- **Jdatetime** for Persian date conversion
- **Uvicorn** ASGI server

### Frontend
- **React** with functional components
- **Axios** for API communication
- **CSS3** with RTL support
- **Responsive design**

## Installation & Setup


### Method 1: Manual Setup:

#### Backend Setup:
```bash

# Create virtual environment
python3 -m venv backend/venv
source backend/venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Run the application
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup:
```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm start
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API status |
| `GET` | `/news/` | Get paginated news |
| `GET` | `/news/search/?q={query}` | Search news |

## Usage

1. **Automatic News Loading**: The application automatically loads news from Varzesh3.com every minute
2. **Browse News**: Scroll through the latest sports news
3. **Search**: Use the search bar to find news by keywords (e.g., "فوتبال", "والیبال")
4. **Read Full Content**: Click "مطالعه کامل" to read full articles in a modal window
5. **View Original**: Click "مشاهده در ورزش سه" to view the original article on Varzesh3.com

## Features Details

### News Scraping
- Scrapes both football and other sports news sections
- Extracts titles, content, images, and publication dates
- Converts Persian dates to Gregorian format automatically
- Prevents duplicate entries using news IDs

### Database Schema
- Stores news articles with complete metadata
- Supports categories and tags
- Maintains publication dates and timestamps
- Includes image URLs for each news item

### User Interface
- Responsive design works on desktop and mobile
- Persian RTL layout support
- Clean modal-based article reading
- Search functionality with instant results
- Category-based news organization

## Configuration

The application uses the following default settings:
- **Backend Port**: 8000
- **Frontend Port**: 3000  
- **Database**: SQLite (varzesh3_news.db)
- **Scraping Interval**: 60 seconds


### Development Tips

- Backend logs will show scraping progress and errors
- Frontend console provides API call debugging information
- Check network tab for API request/response details
