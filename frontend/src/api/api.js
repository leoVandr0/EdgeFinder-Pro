import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API endpoints
export const strengthAPI = {
  getAll: () => api.get('/api/strength/'),
  getByCurrency: (currency) => api.get(`/api/strength/currency/${currency}`),
};

export const insightsAPI = {
  getAll: (limit = 10) => api.get(`/api/insights/?limit=${limit}`),
  getByPair: (pair) => api.get(`/api/insights/pair/${pair}`),
};

export const eventsAPI = {
  getAll: (params = {}) => api.get('/api/events/', { params }),
  getToday: () => api.get('/api/events/today'),
  getHighImpact: () => api.get('/api/events/high-impact'),
};

export const pairCompareAPI = {
  compare: (base, quote) => api.get(`/api/pair-compare/?base=${base}&quote=${quote}`),
  compareDirect: (pair) => api.get(`/api/pair-compare/${pair}`),
};

export const newsAPI = {
  getSummaries: (params = {}) => api.get('/api/news-summary/', { params }),
  getSentiment: () => api.get('/api/news-summary/sentiment'),
  getByCurrency: (currency, limit = 5) => api.get(`/api/news-summary/currency/${currency}?limit=${limit}`),
};

export default api;
