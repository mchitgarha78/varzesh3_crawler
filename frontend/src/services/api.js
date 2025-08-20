import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// add interceptor?
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const getNews = async (skip = 0, limit = 100) => {
  try {
    const response = await api.get(`/news?skip=${skip}&limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching news:', error);
    throw error;
  }
};

export const searchNews = async (query, skip = 0, limit = 100) => {
  try {
    const response = await api.get(`/news/search?q=${encodeURIComponent(query)}&skip=${skip}&limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Error searching news:', error);
    throw error;
  }
};


export default api;