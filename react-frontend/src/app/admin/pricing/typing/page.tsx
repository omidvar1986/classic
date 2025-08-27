'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useState, useEffect } from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';
import AdminDashboardLayout from '@/components/admin/AdminDashboardLayout';

interface TypingPricing {
  pricePerPage: number;
  urgentMultiplier: number;
  bulkDiscount10: number;
  bulkDiscount20: number;
  bulkDiscount50: number;
  isActive: boolean;
}

export default function TypingPricing() {
  const { user } = useAuth();
  const [pricing, setPricing] = useState<TypingPricing>({
    pricePerPage: 0,
    urgentMultiplier: 1.5,
    bulkDiscount10: 0.05,
    bulkDiscount20: 0.1,
    bulkDiscount50: 0.15,
    isActive: true,
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    // Simulate loading pricing
    setTimeout(() => {
      setPricing({
        pricePerPage: 5000,
        urgentMultiplier: 1.5,
        bulkDiscount10: 0.05,
        bulkDiscount20: 0.1,
        bulkDiscount50: 0.15,
        isActive: true,
      });
      setLoading(false);
    }, 1000);
  }, []);

  const handleSave = async () => {
    setSaving(true);
    // Simulate API call
    setTimeout(() => {
      setSaving(false);
      alert('قیمت‌گذاری با موفقیت ذخیره شد!');
    }, 1500);
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <AdminDashboardLayout>
          <div className="animate-pulse">Loading pricing...</div>
        </AdminDashboardLayout>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <AdminDashboardLayout>
        <div className="p-6">
          <h1 className="text-3xl font-bold mb-8 text-gray-800">قیمت‌گذاری خدمات تایپ</h1>
          
          <div className="bg-white rounded-xl shadow-md p-6 mb-6">
            <h2 className="text-xl font-bold mb-6">قیمت‌های پایه</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  قیمت هر صفحه (تومان)
                </label>
                <input
                  type="number"
                  value={pricing.pricePerPage}
                  onChange={(e) => setPricing({ ...pricing, pricePerPage: Number(e.target.value) })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="قیمت هر صفحه"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  ضریب فوری (برای سفارشات فوری)
                </label>
                <input
                  type="number"
                  step="0.1"
                  value={pricing.urgentMultiplier}
                  onChange={(e) => setPricing({ ...pricing, urgentMultiplier: Number(e.target.value) })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="ضریب فوری"
                />
              </div>
            </div>

            <div className="mb-6">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={pricing.isActive}
                  onChange={(e) => setPricing({ ...pricing, isActive: e.target.checked })}
                  className="mr-2"
                />
                <span className="text-sm font-medium text-gray-700">فعال بودن قیمت‌گذاری</span>
              </label>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-md p-6 mb-6">
            <h2 className="text-xl font-bold mb-6">تخفیفات حجمی</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  تخفیف برای 10+ صفحه (درصد)
                </label>
                <input
                  type="number"
                  step="0.01"
                  value={pricing.bulkDiscount10 * 100}
                  onChange={(e) => setPricing({ ...pricing, bulkDiscount10: Number(e.target.value) / 100 })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="درصد تخفیف"
                />
                <p className="text-sm text-gray-500 mt-1">تخفیف: {(pricing.bulkDiscount10 * 100).toFixed(0)}%</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  تخفیف برای 20+ صفحه (درصد)
                </label>
                <input
                  type="number"
                  step="0.01"
                  value={pricing.bulkDiscount20 * 100}
                  onChange={(e) => setPricing({ ...pricing, bulkDiscount20: Number(e.target.value) / 100 })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="درصد تخفیف"
                />
                <p className="text-sm text-gray-500 mt-1">تخفیف: {(pricing.bulkDiscount20 * 100).toFixed(0)}%</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  تخفیف برای 50+ صفحه (درصد)
                </label>
                <input
                  type="number"
                  step="0.01"
                  value={pricing.bulkDiscount50 * 100}
                  onChange={(e) => setPricing({ ...pricing, bulkDiscount50: Number(e.target.value) / 100 })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="درصد تخفیف"
                />
                <p className="text-sm text-gray-500 mt-1">تخفیف: {(pricing.bulkDiscount50 * 100).toFixed(0)}%</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-bold mb-6">پیش‌نمایش قیمت‌گذاری</h2>
            
            <div className="space-y-4">
              <div className="p-4 bg-gray-50 rounded-lg">
                <h3 className="font-medium text-gray-800 mb-2">نمونه محاسبه:</h3>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• سفارش 1 صفحه: {pricing.pricePerPage.toLocaleString()} تومان</li>
                  <li>• سفارش 15 صفحه: {(pricing.pricePerPage * 15 * (1 - pricing.bulkDiscount10)).toLocaleString()} تومان (تخفیف {(pricing.bulkDiscount10 * 100).toFixed(0)}%)</li>
                  <li>• سفارش 25 صفحه: {(pricing.pricePerPage * 25 * (1 - pricing.bulkDiscount20)).toLocaleString()} تومان (تخفیف {(pricing.bulkDiscount20 * 100).toFixed(0)}%)</li>
                  <li>• سفارش فوری 1 صفحه: {(pricing.pricePerPage * pricing.urgentMultiplier).toLocaleString()} تومان</li>
                </ul>
              </div>
            </div>

            <div className="flex justify-end mt-6">
              <button
                onClick={handleSave}
                disabled={saving}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-2 px-6 rounded-lg transition duration-200"
              >
                {saving ? 'در حال ذخیره...' : 'ذخیره قیمت‌گذاری'}
              </button>
            </div>
          </div>
        </div>
      </AdminDashboardLayout>
    </ProtectedRoute>
  );
}
