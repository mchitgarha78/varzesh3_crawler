import React, { useState, useEffect } from 'react';
import NewsList from './components/NewsList';
import SearchBar from './components/SearchBar';
import { getNews, searchNews } from './services/api';
import './App.css';

function App() {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchNews();
  }, []);

  const fetchNews = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getNews();
      setNews(data);
    } catch (error) {
      console.error('Error fetching news:', error);
      setError('خطا در دریافت اخبار. لطفا دوباره تلاش کنید.');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (term) => {
    setSearchTerm(term);
    try {
      setLoading(true);
      setError(null);
      const data = term ? await searchNews(term) : await getNews();
      setNews(data);
    } catch (error) {
      console.error('Error searching news:', error);
      setError('خطا در جستجوی اخبار. لطفا دوباره تلاش کنید.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>خبرخوان ورزشی</h1>
        <div className="header-actions">
          <SearchBar onSearch={handleSearch} />
          <button onClick={fetchNews} className="refresh-button">
            بروزرسانی لیست
          </button>
        </div>
      </header>
      <main>
        {error && (
          <div className="error-message">
            {error}
            <button onClick={fetchNews} className="retry-button">
              تلاش مجدد
            </button>
          </div>
        )}
        {loading ? (
          <div className="loading">
            <p>در حال بارگذاری اخبار...</p>
          </div>
        ) : (
          <NewsList news={news} />
        )}
      </main>
    </div>
  );
}

export default App;