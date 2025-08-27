'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useState, useEffect } from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';
import AdminDashboardLayout from '@/components/admin/AdminDashboardLayout';

interface Package {
  id: number;
  name: string;
  description: string;
  price: number;
  discount: number;
  accessories: string[];
  isActive: boolean;
}

export default function AccessoriesPackages() {
  const { user } = useAuth();
  const [packages, setPackages] = useState<Package[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingPackage, setEditingPackage] = useState<Package | null>(null);

  useEffect(() => {
    // Simulate loading packages
    setTimeout(() => {
      setPackages([
        {
          id: 1,
          name: 'پکیج کامل',
          description: 'شامل چاپ، صحافی و لمینت',
          price: 15000,
          discount: 0.1,
          accessories: ['چاپ رنگی', 'صحافی فنری', 'لمینت'],
          isActive: true
        },
        {
          id: 2,
          name: 'پکیج اقتصادی',
          description: 'بهترین قیمت برای چاپ و صحافی ساده',
          price: 8000,
          discount: 0.05,
          accessories: ['چاپ سیاه سفید', 'صحافی ساده'],
          isActive: true
        }
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const handleAdd = () => {
    setShowAddForm(true);
    setEditingPackage({
      id: 0,
      name: '',
      description: '',
      price: 0,
      discount: 0,
      accessories: [],
      isActive: true
    });
  };

  const handleEdit = (pkg: Package) => {
    setEditingPackage(pkg);
    setShowAddForm(true);
  };

  const handleSave = () => {
    if (editingPackage) {
      if (editingPackage.id === 0) {
        setPackages([...packages, { ...editingPackage, id: Date.now() }]);
      } else {
        setPackages(packages.map(pkg => 
          pkg.id === editingPackage.id ? editingPackage : pkg
        ));
      }
    }
    setShowAddForm(false);
    setEditingPackage(null);
  };

  const handleDelete = (id: number) => {
    if (confirm('آیا از حذف این پکیج مطمئن هستید؟')) {
      setPackages(packages.filter(pkg => pkg.id !== id));
    }
  };

  const toggleActive = (id: number) => {
    setPackages(packages.map(pkg => 
      pkg.id === id ? { ...pkg, isActive: !pkg.isActive } : pkg
    ));
  };

  const addAccessory = (accessory: string) => {
    if (editingPackage && accessory.trim() && !editingPackage.accessories.includes(accessory.trim())) {
      setEditingPackage({
        ...editingPackage,
        accessories: [...editingPackage.accessories, accessory.trim()]
      });
    }
  };

  const removeAccessory = (index: number) => {
    if (editingPackage) {
      setEditingPackage({
        ...editingPackage,
        accessories: editingPackage.accessories.filter((_, i) => i !== index)
      });
    }
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <AdminDashboardLayout>
          <div className="animate-pulse">Loading packages...</div>
        </AdminDashboardLayout>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <AdminDashboardLayout>
        <div className="p-6">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800">مدیریت پکیج‌های لوازم جانبی</h1>
            <button
              onClick={handleAdd}
              className="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg transition duration-200"
            >
              + افزودن پکیج جدید
            </button>
          </div>

          {showAddForm && editingPackage && (
            <div className="bg-white rounded-xl shadow-md p-6 mb-6">
              <h2 className="text-xl font-bold mb-4">
                {editingPackage.id === 0 ? 'افزودن' : 'ویرایش'} پکیج
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    نام پکیج
                  </label>
                  <input
                    type="text"
                    value={editingPackage.name}
                    onChange={(e) => setEditingPackage({ ...editingPackage, name: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="نام پکیج"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    قیمت (تومان)
                  </label>
                  <input
                    type="number"
                    value={editingPackage.price}
                    onChange={(e) => setEditingPackage({ ...editingPackage, price: Number(e.target.value) })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="قیمت"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    درصد تخفیف
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={editingPackage.discount * 100}
                    onChange={(e) => setEditingPackage({ ...editingPackage, discount: Number(e.target.value) / 100 })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="درصد تخفیف"
                  />
                </div>

                <div className="flex items-center">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={editingPackage.isActive}
                      onChange={(e) => setEditingPackage({ ...editingPackage, isActive: e.target.checked })}
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
                  value={editingPackage.description}
                  onChange={(e) => setEditingPackage({ ...editingPackage, description: e.target.value })}
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="توضیحات پکیج"
                />
              </div>

              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  لوازم جانبی موجود در پکیج
                </label>
                <div className="flex mb-2">
                  <input
                    type="text"
                    placeholder="نام لوازم جانبی"
                    onKeyPress={(e) => {
                      if (e.key === 'Enter') {
                        addAccessory(e.currentTarget.value);
                        e.currentTarget.value = '';
                      }
                    }}
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-l-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <button
                    type="button"
                    onClick={(e) => {
                      const input = e.currentTarget.previousSibling as HTMLInputElement;
                      addAccessory(input.value);
                      input.value = '';
                    }}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-r-lg"
                  >
                    افزودن
                  </button>
                </div>
                <div className="space-y-1">
                  {editingPackage.accessories.map((accessory, index) => (
                    <div key={index} className="flex items-center justify-between bg-gray-100 px-3 py-2 rounded">
                      <span>{accessory}</span>
                      <button
                        onClick={() => removeAccessory(index)}
                        className="text-red-600 hover:text-red-800"
                      >
                        حذف
                      </button>
                    </div>
                  ))}
                </div>
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
                      نام پکیج
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      قیمت
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      تخفیف
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      لوازم جانبی
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
                  {packages.map((pkg) => (
                    <tr key={pkg.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">{pkg.name}</div>
                        <div className="text-sm text-gray-500">{pkg.description}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {pkg.price.toLocaleString()} تومان
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        %{(pkg.discount * 100).toFixed(0)}
                      </td>
                      <td className="px-6 py-4">
                        <div className="text-sm text-gray-900">
                          {pkg.accessories.join(', ')}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <button
                          onClick={() => toggleActive(pkg.id)}
                          className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                            pkg.isActive 
                              ? 'bg-green-100 text-green-800 hover:bg-green-200' 
                              : 'bg-red-100 text-red-800 hover:bg-red-200'
                          } transition duration-200`}
                        >
                          {pkg.isActive ? 'فعال' : 'غیرفعال'}
                        </button>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                        <button
                          onClick={() => handleEdit(pkg)}
                          className="text-indigo-600 hover:text-indigo-900 ml-2"
                        >
                          ویرایش
                        </button>
                        <button
                          onClick={() => handleDelete(pkg.id)}
                          className="text-red-600 hover:text-red-900"
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
        </div>
      </AdminDashboardLayout>
    </ProtectedRoute>
  );
}
