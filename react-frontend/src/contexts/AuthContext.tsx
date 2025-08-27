'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { authAPI } from '@/lib/api';

interface User {
  id: number;
  email: string;
  username?: string;
  first_name: string;
  last_name: string;
  is_staff: boolean;
  is_superuser: boolean;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (userData: {
    email: string;
    password: string;
    first_name: string;
    last_name: string;
  }) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const checkAuth = async () => {
    try {
      const token = localStorage.getItem('authToken');
      const savedUser = localStorage.getItem('user');
      
      if (!token) {
        setUser(null);
        setLoading(false);
        return;
      }

      // If we have saved user data, use it immediately to avoid flashing
      if (savedUser) {
        try {
          const userData = JSON.parse(savedUser);
          setUser(userData);
        } catch (e) {
          console.error('Failed to parse saved user data:', e);
        }
      }

      // Then verify with backend
      const response = await authAPI.getProfile();
      if (response.success && response.user) {
        setUser(response.user);
        // Update saved user data
        localStorage.setItem('user', JSON.stringify(response.user));
      } else {
        // Invalid response but not necessarily unauthorized
        console.warn('Profile fetch returned invalid response:', response);
        // If we have saved user data, keep using it
        if (!savedUser) {
          localStorage.removeItem('authToken');
          setUser(null);
        }
      }
    } catch (error: any) {
      console.error('Auth check failed:', error);
      // Only clear auth on actual 401/403 Unauthorized, not network issues
      if (error.response?.status === 401 || error.response?.status === 403) {
        console.log('Clearing auth due to unauthorized access');
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        setUser(null);
      } else {
        // For network errors or other issues, keep the user logged in
        console.log('Keeping user logged in despite error');
        // If we don't have user data and can't fetch it, but have token, keep trying
        const savedUser = localStorage.getItem('user');
        if (savedUser && !user) {
          try {
            const userData = JSON.parse(savedUser);
            setUser(userData);
          } catch (e) {
            console.error('Failed to parse saved user data:', e);
          }
        }
      }
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await authAPI.login(email, password);
      if (response.success && response.user) {
        if (response.token) {
          localStorage.setItem('authToken', response.token);
        }
        // Save user data to localStorage for persistence
        localStorage.setItem('user', JSON.stringify(response.user));
        setUser(response.user);
      } else {
        throw new Error(response.message || 'Login failed');
      }
    } catch (error: any) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const register = async (userData: {
    email: string;
    password: string;
    first_name: string;
    last_name: string;
  }) => {
    try {
      const response = await authAPI.register(userData);
      if (response.success && response.user) {
        if (response.token) {
          localStorage.setItem('authToken', response.token);
        }
        // Save user data to localStorage for persistence
        localStorage.setItem('user', JSON.stringify(response.user));
        setUser(response.user);
      } else {
        throw new Error(response.message || 'Registration failed');
      }
    } catch (error: any) {
      console.error('Registration failed:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      setUser(null);
    }
  };

  useEffect(() => {
    checkAuth();

    // Listen for auth expiration events from API interceptor
    const handleAuthExpiration = () => {
      console.log('Auth expiration event received');
      setUser(null);
    };

    window.addEventListener('auth-expired', handleAuthExpiration);
    
    return () => {
      window.removeEventListener('auth-expired', handleAuthExpiration);
    };
  }, []);

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    checkAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}; 