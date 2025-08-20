import React from 'react';

const NewsList = ({ news }) => {
  if (!news || news.length === 0) {
    return <p style={{ textAlign: 'center', padding: '20px' }}>هیچ خبری یافت نشد.</p>;
  }

  return (
    <div className="news-list">
      {news.map((item) => (
        <div key={item.id} className="news-item">
          <h2>{item.title}</h2>
          
          {item.content && (
            <div className="news-content">
              <p>{item.content.substring(0, 250)}...</p>
            </div>
          )}
          
          <div className="news-meta">
            <span className="news-category">{item.category || 'ورزشی'}</span>
            <span className="news-date">
              {new Date(item.published_date).toLocaleString('fa-IR')}
            </span>
          </div>
          
          <div className="news-actions">
            <a href={item.link} target="_blank" rel="noopener noreferrer" className="news-link">
              مطالعه کامل خبر
            </a>
          </div>
        </div>
      ))}
    </div>
  );
};

export default NewsList;