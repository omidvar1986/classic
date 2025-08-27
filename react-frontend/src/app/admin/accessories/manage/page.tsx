'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useState, useEffect } from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';
import AdminDashboardLayout from '@/components/admin/AdminDashboardLayout';

interface Accessory {
  id: number;
  name: string;
  nameEn: string;
  price: number;
  isActive: boolean;
  description: string;
}

export default function AccessoriesManage() {
  const { user } = useAuth();
  const [accessories, setAccessories] = useState<Accessory[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingAccessory, setEditingAccessory] = useState<Accessory | null>(null);

  useEffect(() => {
    // Simulate loading accessories
    setTimeout(() => {
      setAccessories([
        {
          id: 1,
          name: 'صحافی ساده',
          nameEn: 'Simple Binding',
          price: 2000,
          isActive: true,
          description: 'صحافی ساده با جلد معمولی'
        },
        {
          id: 2,
          name: 'صحافی فنری',
          nameEn: 'Spiral Binding',
          price: 3000,
          isActive: true,
          description: 'صحافی با فنر فلزی'
        },
        {
          id: 3,
          name: 'لمینت',
          nameEn: 'Laminating',
          price: 1500,
          isActive: true,
          description: 'لمینت کردن صفحات'
        }
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const handleAdd = () => {
    setShowAddForm(true);
    setEditingAccessory({
      id: 0,
      name: '',
      nameEn: '',
      price: 0,
      isActive: true,
      description: ''
    });
  };

  const handleEdit = (accessory: Accessory) => {
    setEditingAccessory(accessory);
    setShowAddForm(true);
  };

  const handleSave = () => {
    if (editingAccessory) {
      if (editingAccessory.id === 0) {
        // Add new accessory
        setAccessories([...accessories, { ...editingAccessory, id: Date.now() }]);
      } else {
        // Update existing accessory
        setAccessories(accessories.map(acc => 
          acc.id === editingAccessory.id ? editingAccessory : acc
        ));
      }
    }
    setShowAddForm(false);
    setEditingAccessory(null);
  };

  const handleDelete = (id: number) => {
    if (confirm('آیا از حذف این لوازم جانبی مطمئن هستید؟')) {
      setAccessories(accessories.filter(acc => acc.id !== id));
    }
  };

  const toggleActive = (id: number) => {
    setAccessories(accessories.map(acc => 
      acc.id === id ? { ...acc, isActive: !acc.isActive } : acc
    ));
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <AdminDashboardLayout>
          <div className="animate-pulse">Loading accessories...</div>
        </AdminDashboardLayout>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <AdminDashboardLayout>
        <div className="p-6">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800">مدیریت لوازم جانبی</h1>
            <button
              onClick={handleAdd}
              className="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg transition duration-200"
            >
              + افزودن لوازم جانبی جدید
            </button>
          </div>

          {showAddForm && editingAccessory && (
            <div className="bg-white rounded-xl shadow-md p-6 mb-6">
              <h2 className="text-xl font-bold mb-4">
                {editingAccessory.id === 0 ? 'افزودن' : 'ویرایش'} لوازم جانبی
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    نام فارسی
                  </label>
                  <input
                    type="text"
                    value={editingAccessory.name}
                    onChange={(e) => setEditingAccessory({ ...editingAccessory, name: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="نام فارسی"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    نام انگلیسی
                  </label>
                  <input
                    type="text"
                    value={editingAccessory.nameEn}
                    onChange={(e) => setEditingAccessory({ ...editingAccessory, nameEn: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="English Name"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    قیمت (تومان)
                  </label>
                  <input
                    type="number"
                    value={editingAccessory.price}
                    onChange={(e) => setEditingAccessory({ ...editingAccessory, price: Number(e.target.value) })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="قیمت"
                  />
                </div>

                <div className="flex items-center">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={editingAccessory.isActive}
                      onChange={(e) => setEditingAccessory({ ...editingAccessory, isActive: e.target.checked })}
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
                  value={editingAccessory.description}
                  onChange={(e) => setEditingAccessory({ ...editingAccessory, description: e.target.value })}
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="توضیحات لوازم جانبی"
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
                      نام فارسی
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      نام انگلیسی
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      قیمت
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
                  {accessories.map((accessory) => (
                    <tr key={accessory.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">{accessory.name}</div>
                        <div className="text-sm text-gray-500">{accessory.description}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {accessory.nameEn}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {accessory.price.toLocaleString()} تومان
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <button
                          onClick={() => toggleActive(accessory.id)}
                          className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                            accessory.isActive 
                              ? 'bg-green-100 text-green-800 hover:bg-green-200' 
                              : 'bg-red-100 text-red-800 hover:bg-red-200'
                          } transition duration-200`}
                        >
                          {accessory.isActive ? 'فعال' : 'غیرفعال'}
                        </button>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                        <button
                          onClick={() => handleEdit(accessory)}
                          className="text-indigo-600 hover:text-indigo-900 ml-2"
                        >
                          ویرایش
                        </button>
                        <button
                          onClick={() => handleDelete(accessory.id)}
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
