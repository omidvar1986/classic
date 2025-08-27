'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useState, useEffect } from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';
import AdminDashboardLayout from '@/components/admin/AdminDashboardLayout';

interface PaymentSettings {
  bankAccount: string;
  cardNumber: string;
  shabaNumber: string;
  accountHolder: string;
  isActive: boolean;
}

export default function PaymentSettings() {
  const { user } = useAuth();
  const [settings, setSettings] = useState<PaymentSettings>({
    bankAccount: '',
    cardNumber: '',
    shabaNumber: '',
    accountHolder: '',
    isActive: true,
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    // Simulate loading settings
    setTimeout(() => {
      setSettings({
        bankAccount: '123456789',
        cardNumber: '6037-9911-1234-5678',
        shabaNumber: 'IR123456789123456789123456',
        accountHolder: 'شرکت خدماتی',
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
      alert('تنظیمات با موفقیت ذخیره شد!');
    }, 1500);
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <AdminDashboardLayout>
          <div className="animate-pulse">Loading settings...</div>
        </AdminDashboardLayout>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <AdminDashboardLayout>
        <div className="p-6">
          <h1 className="text-3xl font-bold mb-8 text-gray-800">تنظیمات پرداخت</h1>
          
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-bold mb-6">اطلاعات حساب بانکی</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  شماره حساب
                </label>
                <input
                  type="text"
                  value={settings.bankAccount}
                  onChange={(e) => setSettings({ ...settings, bankAccount: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="شماره حساب را وارد کنید"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  شماره کارت
                </label>
                <input
                  type="text"
                  value={settings.cardNumber}
                  onChange={(e) => setSettings({ ...settings, cardNumber: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="شماره کارت را وارد کنید"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  شماره شبا
                </label>
                <input
                  type="text"
                  value={settings.shabaNumber}
                  onChange={(e) => setSettings({ ...settings, shabaNumber: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="شماره شبا را وارد کنید"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  صاحب حساب
                </label>
                <input
                  type="text"
                  value={settings.accountHolder}
                  onChange={(e) => setSettings({ ...settings, accountHolder: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="نام صاحب حساب را وارد کنید"
                />
              </div>
            </div>

            <div className="mb-6">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={settings.isActive}
                  onChange={(e) => setSettings({ ...settings, isActive: e.target.checked })}
                  className="mr-2"
                />
                <span className="text-sm font-medium text-gray-700">فعال بودن پرداخت آنلاین</span>
              </label>
            </div>

            <div className="flex justify-end">
              <button
                onClick={handleSave}
                disabled={saving}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-2 px-6 rounded-lg transition duration-200"
              >
                {saving ? 'در حال ذخیره...' : 'ذخیره تنظیمات'}
              </button>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-md p-6 mt-6">
            <h2 className="text-xl font-bold mb-6">درگاه‌های پرداخت</h2>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                <div>
                  <h3 className="font-medium text-gray-800">زرین پال</h3>
                  <p className="text-sm text-gray-600">درگاه پرداخت زرین پال</p>
                </div>
                <div className="flex items-center">
                  <span className="text-green-600 text-sm ml-2">فعال</span>
                  <div className="relative inline-block w-10 ml-2 align-middle select-none">
                    <input type="checkbox" name="zarinpal" id="zarinpal" className="checked:bg-green-500 outline-none focus:outline-none right-4 checked:right-0 duration-200 ease-in absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"/>
                    <label htmlFor="zarinpal" className="block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                <div>
                  <h3 className="font-medium text-gray-800">پی‌ای‌کی</h3>
                  <p className="text-sm text-gray-600">درگاه پرداخت پی‌ای‌کی</p>
                </div>
                <div className="flex items-center">
                  <span className="text-gray-600 text-sm ml-2">غیرفعال</span>
                  <div className="relative inline-block w-10 ml-2 align-middle select-none">
                    <input type="checkbox" name="payyk" id="payyk" className="checked:bg-green-500 outline-none focus:outline-none right-4 checked:right-0 duration-200 ease-in absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"/>
                    <label htmlFor="payyk" className="block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </AdminDashboardLayout>
    </ProtectedRoute>
  );
}
