'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

interface ProtectedRouteProps {
  children: React.ReactNode;
  redirectTo?: string;
}

export default function ProtectedRoute({ children, redirectTo = '/login' }: ProtectedRouteProps) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push(redirectTo);
    }
  }, [user, loading, router, redirectTo]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="text-white text-xl">در حال بارگذاری...</div>
      </div>
    );
  }

  if (!user && !loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
        <div className="bg-white/10 border border-white/20 rounded-xl p-10 shadow-lg text-center max-w-lg">
          <h2 className="text-2xl font-semibold text-white mb-2">نشست شما منقضی شده است</h2>
          <p className="text-gray-300 mb-8">برای ادامه، لطفاً دوباره وارد شوید.</p>
          <button
            onClick={() => router.push(redirectTo)}
            className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-medium px-8 py-3 text-lg rounded"
          >
            رفتن به صفحه ورود
          </button>
        </div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return <>{children}</>;
} 