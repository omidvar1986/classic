import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Important for Django session cookies
  timeout: 10000, // 10 second timeout
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Only logout on 401 errors for authenticated endpoints, not on network errors or 404s
    if (error.response?.status === 401) {
      // Check if this is an authenticated endpoint (has Authorization header)
      const hasAuthHeader = error.config?.headers?.Authorization;
      if (hasAuthHeader) {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        console.log('Authentication failed, tokens removed');
        // Dispatch custom event to notify components
        window.dispatchEvent(new CustomEvent('auth-expired'));
      }
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (email: string, password: string) => {
    const response = await api.post('/accounts/api/login/', { email, password });
    return response.data;
  },
  
  register: async (userData: {
    email: string;
    password: string;
    first_name: string;
    last_name: string;
  }) => {
    const response = await api.post('/accounts/api/register/', userData);
    return response.data;
  },
  
  logout: async () => {
    const response = await api.post('/accounts/api/logout/');
    return response.data;
  },
  
  getProfile: async () => {
    const response = await api.get('/accounts/api/profile/');
    return response.data;
  },
};

// Dashboard API
export const dashboardAPI = {
  getDashboard: async () => {
    const response = await api.get('/accounts/dashboard/');
    return response.data;
  },
  
  getPrintOrders: async () => {
    const response = await api.get('/print/my-orders/');
    return response.data;
  },
  
  getTypingOrders: async () => {
    const response = await api.get('/typing/my-orders/');
    return response.data;
  },
  
  getDigitalShopOrders: async () => {
    const response = await api.get('/shop/api/orders/');
    return response.data;
  },
};

// Print Service API
export const printServiceAPI = {
  createOrder: async (orderData: any) => {
    const response = await api.post('/print/', orderData);
    return response.data;
  },
  
  getOrder: async (orderId: number) => {
    const response = await api.get(`/print/order/${orderId}/`);
    return response.data;
  },
  
  trackOrder: async (orderId: number, email: string) => {
    const response = await api.get(`/print/track/?order_id=${orderId}&email=${email}`);
    return response.data;
  },
};

// Typing Service API
export const typingServiceAPI = {
  createOrder: async (orderData: any) => {
    const response = await api.post('/typing/create/', orderData);
    return response.data;
  },
  
  getOrder: async (orderId: number) => {
    const response = await api.get(`/typing/order/${orderId}/`);
    return response.data;
  },
  
  trackOrder: async (orderId: number, email: string) => {
    const response = await api.get(`/typing/track/?order_id=${orderId}&email=${email}`);
    return response.data;
  },
};

// Digital Shop API
export const digitalShopAPI = {
  getProducts: async () => {
    const response = await api.get('/shop/api/products/');
    return response.data;
  },
  
  getProduct: async (productId: string) => {
    const response = await api.get(`/shop/api/product/${productId}/`);
    return response.data;
  },
  
  addToCart: async (productId: number, quantity: number = 1) => {
    const response = await api.post('/shop/api/cart/add/', { product_id: productId, quantity });
    return response.data;
  },
  
  getCart: async () => {
    const response = await api.get('/shop/api/cart/');
    return response.data;
  },
  
  updateCartItem: async (itemId: number, quantity: number) => {
    const response = await api.post(`/shop/api/cart/update/${itemId}/`, { quantity });
    return response.data;
  },
  
  removeCartItem: async (itemId: number) => {
    const response = await api.post(`/shop/api/cart/remove/${itemId}/`);
    return response.data;
  },
  
  checkout: async (checkoutData: any) => {
    const response = await api.post('/shop/api/create-order/', checkoutData);
    return response.data;
  },
  uploadPaymentReceipt: async (orderId: number, formData: FormData) => {
    const response = await api.post(`/shop/api/orders/${orderId}/payment-receipts/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
  
  getDigitalShopOrders: async () => {
    const response = await api.get('/shop/api/orders/');
    return response.data;
  },
  
  // Helper to get full image URL
  getImageUrl: (imagePath: string) => {
    if (!imagePath) return null;
    if (imagePath.startsWith('http')) return imagePath;
    const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
    return `${baseURL}${imagePath}`;
  },
};

export default api;

// Admin API for managing the system
export const adminAPI = {
  // Product Management
  getAdminProducts: async () => {
    const response = await api.get('/shop/api/products/');
    return response.data;
  },
  
  createProduct: async (productData: any) => {
    const response = await api.post('/shop/api/admin/products/create/', productData);
    return response.data;
  },
  
  updateProduct: async (productId: number, productData: any) => {
    const response = await api.put(`/shop/api/admin/products/${productId}/`, productData);
    return response.data;
  },
  
  deleteProduct: async (productId: number) => {
    const response = await api.delete(`/shop/api/admin/products/${productId}/`);
    return response.data;
  },
  
  // Category Management
  getAdminCategories: async () => {
    const response = await api.get('/shop/api/admin/categories/');
    return response.data;
  },
  
  createCategory: async (categoryData: any) => {
    const response = await api.post('/shop/api/admin/categories/create/', categoryData);
    return response.data;
  },
  
  updateCategory: async (categoryId: number, categoryData: any) => {
    const response = await api.put(`/shop/api/admin/categories/${categoryId}/`, categoryData);
    return response.data;
  },
  
  deleteCategory: async (categoryId: number) => {
    const response = await api.delete(`/shop/api/admin/categories/${categoryId}/`);
    return response.data;
  },
  
  // Brand Management
  getAdminBrands: async () => {
    const response = await api.get('/shop/api/admin/brands/');
    return response.data;
  },
  
  createBrand: async (brandData: any) => {
    const response = await api.post('/shop/api/admin/brands/create/', brandData);
    return response.data;
  },
  
  updateBrand: async (brandId: number, brandData: any) => {
    const response = await api.put(`/shop/api/admin/brands/${brandId}/`, brandData);
    return response.data;
  },
  
  deleteBrand: async (brandId: number) => {
    const response = await api.delete(`/shop/api/admin/brands/${brandId}/`);
    return response.data;
  },
}; 