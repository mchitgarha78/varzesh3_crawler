import React, { useState } from 'react';
import NewsModal from './NewsModal';

const NewsList = ({ news }) => {
  const [selectedNews, setSelectedNews] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  if (!news || news.length === 0) {
    return <p style={{ textAlign: 'center', padding: '20px' }}>هیچ خبری یافت نشد.</p>;
  }

  const openModal = (newsItem) => {
    setSelectedNews(newsItem);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedNews(null);
  };

  return (
    <>
      <div className="news-list">
        {news.map((item) => (
          <div key={item.id} className="news-item">
            <div className="news-header">
              {item.image_url && (
                <img 
                  src={item.image_url} 
                  alt={item.title}
                  className="news-image"
                  onError={(e) => {
                    e.target.style.display = 'none';
                  }}
                />
              )}
              <h2>{item.title}</h2>
            </div>
            
            {item.content && (
              <div className="news-content">
                <p>{item.content.substring(0, 200)}...</p>
              </div>
            )}
            
            <div className="news-meta">
              <span className="news-category">{item.category || 'ورزشی'}</span>
              <span className="news-date">
                {new Date(item.published_date).toLocaleString('fa-IR')}
              </span>
            </div>
            
            <div className="news-actions">
              <a 
                href={item.link} 
                target="_blank" 
                rel="noopener noreferrer" 
                className="news-link"
              >
                مشاهده در ورزش سه
              </a>
              <button 
                className="read-more-btn"
                onClick={() => openModal(item)}
              >
                مطالعه کامل
              </button>
            </div>
          </div>
        ))}
      </div>

      <NewsModal 
        news={selectedNews} 
        isOpen={isModalOpen} 
        onClose={closeModal} 
      />
    </>
  );
};

export default NewsList;