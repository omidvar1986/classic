'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useState, useEffect } from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';
import AdminDashboardLayout from '@/components/admin/AdminDashboardLayout';

interface Category {
  id: number;
  name: string;
  description: string;
  isActive: boolean;
  productCount: number;
  parentId?: number;
}

export default function ShopCategories() {
  const { user } = useAuth();
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingCategory, setEditingCategory] = useState<Category | null>(null);

  useEffect(() => {
    // Simulate loading categories
    setTimeout(() => {
      setCategories([
        {
          id: 1,
          name: 'کامپیوتر و لپ‌تاپ',
          description: 'دسته‌بندی مربوط به کامپیوتر، لپ‌تاپ و قطعات',
          isActive: true,
          productCount: 15
        },
        {
          id: 2,
          name: 'موبایل و تبلت',
          description: 'گوشی‌های هوشمند، تبلت و لوازم جانبی',
          isActive: true,
          productCount: 25
        },
        {
          id: 3,
          name: 'لوازم جانبی',
          description: 'موس، کیبورد، هدفون و سایر لوازم جانبی',
          isActive: true,
          productCount: 40
        },
        {
          id: 4,
          name: 'صوتی و تصویری',
          description: 'سیستم‌های صوتی، اسپیکر، هدفون',
          isActive: false,
          productCount: 8
        }
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const handleAdd = () => {
    setShowAddForm(true);
    setEditingCategory({
      id: 0,
      name: '',
      description: '',
      isActive: true,
      productCount: 0
    });
  };

  const handleEdit = (category: Category) => {
    setEditingCategory(category);
    setShowAddForm(true);
  };

  const handleSave = () => {
    if (editingCategory) {
      if (editingCategory.id === 0) {
        setCategories([...categories, { ...editingCategory, id: Date.now() }]);
      } else {
        setCategories(categories.map(cat => 
          cat.id === editingCategory.id ? editingCategory : cat
        ));
      }
    }
    setShowAddForm(false);
    setEditingCategory(null);
  };

  const handleDelete = (id: number) => {
    const category = categories.find(cat => cat.id === id);
    if (category && category.productCount > 0) {
      alert('نمی‌توان دسته‌بندی حاوی محصول را حذف کرد!');
      return;
    }
    
    if (confirm('آیا از حذف این دسته‌بندی مطمئن هستید؟')) {
      setCategories(categories.filter(cat => cat.id !== id));
    }
  };

  const toggleActive = (id: number) => {
    setCategories(categories.map(cat => 
      cat.id === id ? { ...cat, isActive: !cat.isActive } : cat
    ));
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <AdminDashboardLayout>
          <div className="animate-pulse">Loading categories...</div>
        </AdminDashboardLayout>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <AdminDashboardLayout>
        <div className="p-6">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800">مدیریت دسته‌بندی‌های فروشگاه</h1>
            <button
              onClick={handleAdd}
              className="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg transition duration-200"
            >
              + افزودن دسته‌بندی جدید
            </button>
          </div>

          {/* Category Statistics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white rounded-xl shadow-md p-6">
              <div className="text-2xl font-bold text-blue-600 mb-2">
                {categories.length}
              </div>
              <div className="text-sm text-gray-600">کل دسته‌بندی‌ها</div>
            </div>
            
            <div className="bg-white rounded-xl shadow-md p-6">
              <div className="text-2xl font-bold text-green-600 mb-2">
                {categories.filter(cat => cat.isActive).length}
              </div>
              <div className="text-sm text-gray-600">دسته‌بندی‌های فعال</div>
            </div>
            
            <div className="bg-white rounded-xl shadow-md p-6">
              <div className="text-2xl font-bold text-purple-600 mb-2">
                {categories.reduce((sum, cat) => sum + cat.productCount, 0)}
              </div>
              <div className="text-sm text-gray-600">کل محصولات</div>
            </div>
          </div>

          {showAddForm && editingCategory && (
            <div className="bg-white rounded-xl shadow-md p-6 mb-6">
              <h2 className="text-xl font-bold mb-4">
                {editingCategory.id === 0 ? 'افزودن' : 'ویرایش'} دسته‌بندی
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    نام دسته‌بندی
                  </label>
                  <input
                    type="text"
                    value={editingCategory.name}
                    onChange={(e) => setEditingCategory({ ...editingCategory, name: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="نام دسته‌بندی"
                  />
                </div>

                <div className="flex items-center">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={editingCategory.isActive}
                      onChange={(e) => setEditingCategory({ ...editingCategory, isActive: e.target.checked })}
                      className="mr-2"
                    />
                    <span className="text-sm font-medium text-gray-700">فعال</span>
                  </label>
                </div>
              </div>

              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  توضیحات
                </label>
                <textarea
                  value={editingCategory.description}
                  onChange={(e) => setEditingCategory({ ...editingCategory, description: e.target.value })}
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="توضیحات دسته‌بندی"
                />
              </div>

              <div className="flex justify-end space-x-4">
                <button
                  onClick={() => setShowAddForm(false)}
                  className="bg-gray-500 hover:bg-gray-600 text-white font-medium py-2 px-4 rounded-lg transition duration-200 ml-2"
                >
                  انصراف
                </button>
                <button
                  onClick={handleSave}
                  className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition duration-200"
                >
                  ذخیره
                </button>
              </div>
            </div>
          )}

          <div className="bg-white rounded-xl shadow-md">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      نام دسته‌بندی
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      تعداد محصولات
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      وضعیت
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      عملیات
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {categories.map((category) => (
                    <tr key={category.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">{category.name}</div>
                        <div className="text-sm text-gray-500">{category.description}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                          {category.productCount} محصول
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <button
                          onClick={() => toggleActive(category.id)}
                          className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                            category.isActive 
                              ? 'bg-green-100 text-green-800 hover:bg-green-200' 
                              : 'bg-red-100 text-red-800 hover:bg-red-200'
                          } transition duration-200`}
                        >
                          {category.isActive ? 'فعال' : 'غیرفعال'}
                        </button>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                        <button
                          onClick={() => handleEdit(category)}
                          className="text-indigo-600 hover:text-indigo-900 ml-2"
                        >
                          ویرایش
                        </button>
                        <button
                          onClick={() => handleDelete(category.id)}
                          className={`${
                            category.productCount > 0 
                              ? 'text-gray-400 cursor-not-allowed' 
                              : 'text-red-600 hover:text-red-900'
                          }`}
                          disabled={category.productCount > 0}
                        >
                          حذف
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-yellow-800">نکته مهم</h3>
                <div className="mt-2 text-sm text-yellow-700">
                  <p>دسته‌بندی‌هایی که دارای محصول هستند قابل حذف نیستند. ابتدا محصولات را به دسته‌بندی دیگری منتقل کنید یا حذف کنید.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </AdminDashboardLayout>
    </ProtectedRoute>
  );
}
