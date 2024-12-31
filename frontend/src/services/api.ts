import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token de autenticação
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const authService = {
  login: async (username: string, password: string) => {
    const response = await api.post('/token', { username, password });
    return response.data;
  },
  register: async (userData: {
    username: string, 
    email: string, 
    password: string, 
    nostr_pubkey: string
  }) => {
    const response = await api.post('/register', userData);
    return response.data;
  },
};

export const orderService = {
  createOrder: async (orderData: {
    pair: string,
    type: 'buy' | 'sell',
    price: number,
    amount: number
  }) => {
    const response = await api.post('/orders', orderData);
    return response.data;
  },
  getOrderBook: async (pair: string) => {
    const response = await api.get(`/orderbook/${pair}`);
    return response.data;
  },
};

export const walletService = {
  getWallets: async () => {
    const response = await api.get('/wallets');
    return response.data;
  },
  deposit: async (currency: string, amount: number) => {
    const response = await api.post('/wallets/deposit', { currency, amount });
    return response.data;
  },
};

export default api;
