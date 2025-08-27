'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useState, useEffect } from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';
import AdminDashboardLayout from '@/components/admin/AdminDashboardLayout';
import { adminAPI } from '@/lib/api';

interface Product {
  id: number;
  name: string;
  description: string;
  short_description?: string;
  price: number;
  compare_price?: number;
  stock_quantity: number;
  sku: string;
  category: {
    id: number;
    name: string;
  } | null;
  brand: {
    id: number;
    name: string;
  } | null;
  images: Array<{
    id: number;
    image: string;
  }>;
  is_active: boolean;
  is_featured: boolean;
  is_new: boolean;
  is_on_sale: boolean;
  condition: string;
  created_at: string;
}

export default function ShopProducts() {
  const { user } = useAuth();
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [productImages, setProductImages] = useState<string[]>([]);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await adminAPI.getAdminProducts();
      if (response.success) {
        setProducts(response.products);
      } else {
        setError('خطا در دریافت محصولات');
      }
    } catch (error) {
      console.error('Error fetching products:', error);
      setError('خطا در ارتباط با سرور');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setShowAddForm(true);
    setEditingProduct({
      id: 0,
      name: '',
      description: '',
      short_description: '',
      price: 0,
      compare_price: 0,
      stock_quantity: 0,
      sku: '',
      category: null,
      brand: null,
      images: [],
      is_active: true,
      is_featured: false,
      is_new: true,
      is_on_sale: false,
      condition: 'new',
      created_at: new Date().toISOString()
    });
    setError(null);
    setSuccess(null);
  };

  const handleEdit = (product: Product) => {
    setEditingProduct(product);
    setShowAddForm(true);
    setError(null);
    setSuccess(null);
  };

  const handleSave = async () => {
    if (!editingProduct) return;
    
    try {
      setSaving(true);
      setError(null);
      
      if (editingProduct.id === 0) {
        // Create new product
        const productData = {
          name: editingProduct.name,
          description: editingProduct.description,
          short_description: editingProduct.short_description,
          price: editingProduct.price,
          compare_price: editingProduct.compare_price,
          stock_quantity: editingProduct.stock_quantity,
          sku: editingProduct.sku || `SKU-${Date.now()}`,
          category_id: editingProduct.category?.id,
          brand_id: editingProduct.brand?.id,
          is_active: editingProduct.is_active,
          is_featured: editingProduct.is_featured,
          is_new: editingProduct.is_new,
          is_on_sale: editingProduct.is_on_sale,
          condition: editingProduct.condition,
        };
        
        const response = await adminAPI.createProduct(productData);
        if (response.success) {
          setSuccess('محصول با موفقیت ایجاد شد');
          setShowAddForm(false);
          setEditingProduct(null);
          fetchProducts(); // Refresh the list
        } else {
          setError(response.message || 'خطا در ایجاد محصول');
        }
      } else {
        // Update existing product
        const productData = {
          name: editingProduct.name,
          description: editingProduct.description,
          short_description: editingProduct.short_description,
          price: editingProduct.price,
          compare_price: editingProduct.compare_price,
          stock_quantity: editingProduct.stock_quantity,
          sku: editingProduct.sku,
          category_id: editingProduct.category?.id,
          brand_id: editingProduct.brand?.id,
          is_active: editingProduct.is_active,
          is_featured: editingProduct.is_featured,
          is_new: editingProduct.is_new,
          is_on_sale: editingProduct.is_on_sale,
          condition: editingProduct.condition,
        };
        
        const response = await adminAPI.updateProduct(editingProduct.id, productData);
        if (response.success) {
          setSuccess('محصول با موفقیت به‌روزرسانی شد');
          setShowAddForm(false);
          setEditingProduct(null);
          fetchProducts(); // Refresh the list
        } else {
          setError(response.message || 'خطا در به‌روزرسانی محصول');
        }
      }
    } catch (error) {
      console.error('Error saving product:', error);
      setError('خطا در ارتباط با سرور');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('آیا از حذف این محصول مطمئن هستید؟')) return;
    
    try {
      const response = await adminAPI.deleteProduct(id);
      if (response.success) {
        setSuccess('محصول با موفقیت حذف شد');
        fetchProducts(); // Refresh the list
      } else {
        setError(response.message || 'خطا در حذف محصول');
      }
    } catch (error) {
      console.error('Error deleting product:', error);
      setError('خطا در ارتباط با سرور');
    }
  };

  const toggleActive = async (id: number) => {
    try {
      const product = products.find(p => p.id === id);
      if (!product) return;
      
      const response = await adminAPI.updateProduct(id, {
        is_active: !product.is_active
      });
      
      if (response.success) {
        fetchProducts(); // Refresh the list
      } else {
        setError(response.message || 'خطا در تغییر وضعیت محصول');
      }
    } catch (error) {
      console.error('Error toggling product status:', error);
      setError('خطا در ارتباط با سرور');
    }
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files) {
      const newImages: string[] = [];
      Array.from(files).forEach(file => {
        const reader = new FileReader();
        reader.onload = (e) => {
          if (e.target?.result) {
            newImages.push(e.target.result as string);
            if (newImages.length === files.length) {
              setProductImages(prev => [...prev, ...newImages]);
              if (editingProduct) {
                // Convert string images to proper format for now
                const imageObjects = newImages.map((img, index) => ({
                  id: -(index + 1), // Temporary negative ID for new images
                  image: img
                }));
                setEditingProduct({
                  ...editingProduct,
                  images: [...(editingProduct.images || []), ...imageObjects]
                });
              }
            }
          }
        };
        reader.readAsDataURL(file);
      });
    }
  };

  const removeImage = (index: number) => {
    const updatedImages = productImages.filter((_, i) => i !== index);
    setProductImages(updatedImages);
    if (editingProduct) {
      // Remove the image at the specified index
      const updatedProductImages = editingProduct.images.filter((_, i) => i !== index);
      setEditingProduct({
        ...editingProduct,
        images: updatedProductImages
      });
    }
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <AdminDashboardLayout>
          <div className="animate-pulse">Loading products...</div>
        </AdminDashboardLayout>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <AdminDashboardLayout>
        <div className="p-6">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800">مدیریت محصولات فروشگاه</h1>
            <button
              onClick={handleAdd}
              className="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg transition duration-200"
            >
              + افزودن محصول جدید
            </button>
          </div>

          {/* Success and Error Messages */}
          {success && (
            <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
              {success}
            </div>
          )}
          
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
              {error}
            </div>
          )}

          {showAddForm && editingProduct && (
            <div className="bg-white rounded-xl shadow-md p-6 mb-6">
              <h2 className="text-xl font-bold mb-4">
                {editingProduct.id === 0 ? 'افزودن' : 'ویرایش'} محصول
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    نام محصول
                  </label>
                  <input
                    type="text"
                    value={editingProduct.name}
                    onChange={(e) => setEditingProduct({ ...editingProduct, name: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="نام محصول"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    قیمت (تومان)
                  </label>
                  <input
                    type="number"
                    value={editingProduct.price}
                    onChange={(e) => setEditingProduct({ ...editingProduct, price: Number(e.target.value) })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="قیمت"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    موجودی
                  </label>
                  <input
                    type="number"
                    value={editingProduct.stock_quantity}
                    onChange={(e) => setEditingProduct({ ...editingProduct, stock_quantity: Number(e.target.value) })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="موجودی"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    دسته‌بندی
                  </label>
                  <input
                    type="text"
                    value={editingProduct.category?.name || ''}
                    onChange={(e) => setEditingProduct({ ...editingProduct, category: { id: 0, name: e.target.value } })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="دسته‌بندی"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    برند
                  </label>
                  <input
                    type="text"
                    value={editingProduct.brand?.name || ''}
                    onChange={(e) => setEditingProduct({ ...editingProduct, brand: { id: 0, name: e.target.value } })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="برند"
                  />
                </div>

                <div className="flex items-center">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={editingProduct.is_active}
                      onChange={(e) => setEditingProduct({ ...editingProduct, is_active: e.target.checked })}
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
                  value={editingProduct.description}
                  onChange={(e) => setEditingProduct({ ...editingProduct, description: e.target.value })}
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="توضیحات محصول"
                />
              </div>

              {/* Image Upload Section */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  تصاویر محصول
                </label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
                  <div className="text-center">
                    <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                      <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                    <div className="mt-4">
                      <label htmlFor="product-images" className="cursor-pointer">
                        <span className="mt-2 block text-sm font-medium text-gray-900">
                          تصاویر را اینجا بکشید یا کلیک کنید
                        </span>
                        <input
                          id="product-images"
                          type="file"
                          multiple
                          accept="image/*"
                          className="hidden"
                          onChange={handleImageUpload}
                        />
                      </label>
                      <p className="mt-1 text-xs text-gray-500">PNG, JPG, GIF تا 10MB</p>
                    </div>
                  </div>
                </div>
                
                {/* Display uploaded images */}
                {(editingProduct?.images && editingProduct.images.length > 0) && (
                  <div className="mt-4">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      {editingProduct.images.map((image, index) => (
                        <div key={index} className="relative">
                          <img
                            src={image.image}
                            alt={`Product ${index + 1}`}
                            className="w-full h-24 object-cover rounded-lg border border-gray-200"
                          />
                          <button
                            type="button"
                            onClick={() => removeImage(index)}
                            className="absolute -top-2 -right-2 bg-red-500 hover:bg-red-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs"
                          >
                            ×
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
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
                  disabled={saving}
                  className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-2 px-4 rounded-lg transition duration-200"
                >
                  {saving ? 'در حال ذخیره...' : 'ذخیره'}
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
                      محصول
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      قیمت
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      موجودی
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      دسته‌بندی
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      برند
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
                  {products.map((product) => (
                    <tr key={product.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">{product.name}</div>
                        <div className="text-sm text-gray-500 max-w-xs truncate">{product.description}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {product.price.toLocaleString()} تومان
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          product.stock_quantity > 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }`}>
                          {product.stock_quantity > 0 ? `${product.stock_quantity} عدد` : 'ناموجود'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {product.category?.name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {product.brand?.name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <button
                          onClick={() => toggleActive(product.id)}
                          className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                            product.is_active 
                              ? 'bg-green-100 text-green-800 hover:bg-green-200' 
                              : 'bg-red-100 text-red-800 hover:bg-red-200'
                          } transition duration-200`}
                        >
                          {product.is_active ? 'فعال' : 'غیرفعال'}
                        </button>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                        <button
                          onClick={() => handleEdit(product)}
                          className="text-indigo-600 hover:text-indigo-900 ml-2"
                        >
                          ویرایش
                        </button>
                        <button
                          onClick={() => handleDelete(product.id)}
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
