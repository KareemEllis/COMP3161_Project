import axios from 'axios';

// Replace this URL with your Flask API's base URL.
const API_BASE_URL = 'http://localhost:8080';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  // You can set common headers here, like authorization tokens, if needed.
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
