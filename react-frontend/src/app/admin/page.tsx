'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import ProtectedRoute from '@/components/ProtectedRoute';
import AdminDashboardLayout from '@/components/admin/AdminDashboardLayout';
import AdminOverview from '@/components/admin/AdminOverview';

function AdminDashboardContent() {
  const { user } = useAuth();
  
  // Check if user is staff/admin
  if (!user?.is_staff && !user?.is_superuser) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-900 to-red-800">
        <div className="text-center p-8 bg-white/10 rounded-xl">
          <h1 className="text-2xl font-bold text-white mb-4">دسترسی محدود</h1>
          <p className="text-red-200">شما اجازه دسترسی به پنل مدیریت را ندارید.</p>
        </div>
      </div>
    );
  }

  return (
    <AdminDashboardLayout>
      <AdminOverview />
    </AdminDashboardLayout>
  );
}

export default function AdminDashboardPage() {
  return (
    <ProtectedRoute>
      <AdminDashboardContent />
    </ProtectedRoute>
  );
}
