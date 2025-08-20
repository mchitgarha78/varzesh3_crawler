import React, { useState } from 'react';

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleInputChange = (e) => {
    const value = e.target.value;
    setQuery(value);  
    onSearch(value);  
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);  
  };

  return (
    <form onSubmit={handleSubmit} className="search-bar">
      <input
        type="text"
        placeholder="جستجوی اخبار..."
        value={query}
        onChange={handleInputChange}
      />
      <button type="submit">جستجو</button>
    </form>
  );
};

export default SearchBar;