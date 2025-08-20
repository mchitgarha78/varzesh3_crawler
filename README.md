# Varzesh3 News Reader

A web application that crawls and displays news from Varzesh3.com (a popular Persian sports news website) with a modern Python backend and React frontend.

## Features

- **Automated News Crawling**: Periodically scrapes news from Varzesh3.com
- **SQLite Database**: Stores news articles with ORM (SQLAlchemy)
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **React Frontend**: Modern responsive UI with Persian (RTL) support
- **Modal View**: Read full articles without leaving the site
- **Search Functionality**: Full-text search across news titles and content
- **Real-time Updates**: Background scraping every minute
- **Docker Support**: Complete containerization with Docker Compose
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

### DevOps
- **Docker & Docker Compose**
- **Multi-stage builds**
- **Health checks**
- **Container orchestration**

## Installation & Setup

### Method 1: Docker Compose (Recommended)

1. **Clone and setup**:
   ```bash
   git clone https://github.com/mchitgarha78/varzesh3_crawler.git
   cd varzesh3-news-reader
   ```

2. **Run with Docker**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Method 2: Manual Setup (Development)

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

# Fix OpenSSL issue
export NODE_OPTIONS=--openssl-legacy-provider

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

## Docker Commands

```bash
# Build and start containers
docker-compose up --build

# Start in detached mode
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs frontend

# Remove volumes (complete cleanup)
docker-compose down -v
```

## Troubleshooting

### Common Docker Issues

1. **Port conflicts**: Ensure ports 3000 and 8000 are available
2. **Build failures**: Check Docker daemon is running
3. **Container not starting**: Check logs with `docker-compose logs`
4. **OpenSSL issues**: NODE_OPTIONS is set to handle legacy providers

### Database Persistence

The SQLite database is persisted in a Docker volume (`backend_data`) to prevent data loss between container restarts.
