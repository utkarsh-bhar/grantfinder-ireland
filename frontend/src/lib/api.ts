import axios from 'axios';
import type { ProfileData, ScanResponse, AuthTokens, Grant } from '@/types';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || '/api/v1',
  headers: { 'Content-Type': 'application/json' },
});

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Auto-refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const { data } = await axios.post('/api/v1/auth/refresh', {
            refresh_token: refreshToken,
          });
          localStorage.setItem('access_token', data.access_token);
          localStorage.setItem('refresh_token', data.refresh_token);
          original.headers.Authorization = `Bearer ${data.access_token}`;
          return api(original);
        }
      } catch {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      }
    }
    return Promise.reject(error);
  }
);

// ─── Auth ───────────────────────────────────────────────────────────────────

export const authAPI = {
  register: (email: string, password: string) =>
    api.post<AuthTokens>('/auth/register', { email, password }),

  login: (email: string, password: string) =>
    api.post<AuthTokens>('/auth/login', { email, password }),

  me: () => api.get('/auth/me'),
};

// ─── Profile ────────────────────────────────────────────────────────────────

export const profileAPI = {
  get: () => api.get('/profile'),
  save: (data: ProfileData) => api.post('/profile', data),
  update: (data: Partial<ProfileData>) => api.patch('/profile', data),
};

// ─── Scan ───────────────────────────────────────────────────────────────────

export const scanAPI = {
  anonymous: (data: ProfileData) =>
    api.post<ScanResponse>('/scan/anonymous', data),
  run: () => api.post<ScanResponse>('/scan'),
  latest: () => api.get<ScanResponse>('/scan/results'),
  history: () => api.get('/scan/history'),
};

// ─── Grants ─────────────────────────────────────────────────────────────────

export const grantsAPI = {
  list: (page = 1, category?: string) =>
    api.get('/grants', { params: { page, category } }),
  get: (slug: string) => api.get<Grant>(`/grants/${slug}`),
  search: (q: string) => api.get('/grants/search', { params: { q } }),
  categories: () => api.get('/grants/categories'),
  steps: (slug: string) => api.get(`/grants/${slug}/steps`),
  documents: (slug: string) => api.get(`/grants/${slug}/documents`),
};

// ─── Reports ─────────────────────────────────────────────────────────────────

export const reportsAPI = {
  downloadPDF: (profileData: ProfileData) =>
    api.post('/reports/download', profileData, {
      responseType: 'blob',
    }),
};

// ─── Chat ───────────────────────────────────────────────────────────────────

export const chatAPI = {
  ask: (question: string, grant_slug?: string) =>
    api.post('/chat', { question, grant_slug }),
};

// ─── Payments ───────────────────────────────────────────────────────────────

export const paymentsAPI = {
  checkout: (price_id: string) =>
    api.post('/payments/checkout', { price_id }),
  status: () => api.get('/payments/status'),
};

export default api;
