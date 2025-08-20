import React from 'react';
import './NewsModal.css';

const NewsModal = ({ news, isOpen, onClose }) => {
  if (!isOpen || !news) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{news.title}</h2>
          <button className="modal-close" onClick={onClose}>
            ×
          </button>
        </div>
        
        <div className="modal-body">
          {news.image_url && (
            <img 
              src={news.image_url} 
              alt={news.title}
              className="modal-image"
              onError={(e) => {
                e.target.style.display = 'none';
              }}
            />
          )}
          
          <div className="news-full-content">
            {news.content.split('\n\n').map((paragraph, index) => (
              <p key={index}>{paragraph}</p>
            ))}
          </div>
        </div>
        
        <div className="modal-footer">
          <span className="news-category">{news.category || 'ورزشی'}</span>
          <span className="news-date">
            {new Date(news.published_date).toLocaleString('fa-IR')}
          </span>
          <a 
            href={news.link} 
            target="_blank" 
            rel="noopener noreferrer" 
            className="original-link"
          >
            مشاهده در ورزش سه
          </a>
        </div>
      </div>
    </div>
  );
};

export default NewsModal;