'use client';

import { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import ProtectedRoute from '@/components/ProtectedRoute';
import Link from 'next/link';
import { ArrowLeft, FileText, Upload, Plus, Minus, Calculator, User, Phone, Mail } from 'lucide-react';
import { GlowCard } from '@/components/ui/spotlight-card';

function TypingServiceContent() {
  const { user } = useAuth();
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [formData, setFormData] = useState({
    user_name: user?.first_name + ' ' + user?.last_name || '',
    user_email: user?.email || '',
    user_phone: '',
    description: '',
    page_count: 1,
    delivery_option: 'email',
    document_file: null as File | null,
    accessories: [] as Array<{id: number, quantity: number, price: number}>
  });
  const [accessories, setAccessories] = useState<any>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loadingAccessories, setLoadingAccessories] = useState(true);
  const [dragActive, setDragActive] = useState(false);

  useEffect(() => {
    // Fetch accessories when component mounts
    fetchAccessories();
  }, []);

  // Fetch accessories function
  const fetchAccessories = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/typing/api/accessories/', {
        credentials: 'include'
      });
      const result = await response.json();
      if (result.success) {
        setAccessories(result.accessories_by_category);
      }
    } catch (error) {
      console.error('Error fetching accessories:', error);
    } finally {
      setLoadingAccessories(false);
    }
  };

  // Handle form field changes
  const handleChange = (e: any) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  // Handle file upload
  const handleFileSelect = (files: FileList | null) => {
    if (!files || files.length === 0) return;
    
    const file = files[0];
    const allowedTypes = ['.doc', '.docx', '.pdf', '.txt'];
    const fileExt = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    
    if (!allowedTypes.includes(fileExt)) {
      setError('فرمت فایل پشتیبانی نمی‌شود. لطفاً فایل DOC، DOCX، PDF یا TXT انتخاب کنید.');
      return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
      setError('حجم فایل باید کمتر از 10 مگابایت باشد.');
      return;
    }
    
    setFormData(prev => ({ ...prev, document_file: file }));
    setError('');
  };

  // Handle drag and drop
  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    handleFileSelect(e.dataTransfer.files);
  };

  // Handle accessory selection
  const handleAccessory = (id: number, checked: boolean, price: number) => {
    setFormData(prev => {
      let accs = [...prev.accessories];
      if (checked) {
        accs.push({ id, quantity: 1, price });
      } else {
        accs = accs.filter(a => a.id !== id);
      }
      return { ...prev, accessories: accs };
    });
  };

  // Handle accessory quantity change
  const handleAccessoryQuantity = (id: number, change: number) => {
    setFormData(prev => {
      const accs = [...prev.accessories];
      const index = accs.findIndex(a => a.id === id);
      if (index !== -1) {
        accs[index].quantity = Math.max(1, accs[index].quantity + change);
      }
      return { ...prev, accessories: accs };
    });
  };

  // Format file size
  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' bytes';
    else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    else return (bytes / 1048576).toFixed(1) + ' MB';
  };

  // Calculate total price
  const calculatePrice = () => {
    let total = 100000 * formData.page_count; // base price per page
    for (const acc of formData.accessories) {
      total += acc.price * acc.quantity;
    }
    return total;
  };

  // Handle form submit
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch('http://127.0.0.1:8000/typing/api/create/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          user_name: formData.user_name,
          user_email: formData.user_email,
          user_phone: formData.user_phone,
          description: formData.description,
          page_count: formData.page_count,
          delivery_option: formData.delivery_option,
          accessories: formData.accessories
        })
      });

      const result = await response.json();

      if (result.success) {
        setSuccess('سفارش تایپ با موفقیت ثبت شد!');
        setTimeout(() => {
          router.push('/typing-orders');
        }, 2000);
      } else {
        setError(result.message || 'خطا در ثبت سفارش');
      }
    } catch (err) {
      setError('خطا در ثبت سفارش. لطفاً دوباره تلاش کنید.');
      console.error('Error creating order:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
      {/* Header */}
      <div className="max-w-4xl mx-auto mb-8">
        <div className="flex items-center gap-4 mb-6">
          <Link href="/dashboard">
            <Button variant="outline" className="border-white/20 text-white hover:bg-white/10">
              <ArrowLeft className="h-4 w-4 mr-2" />
              بازگشت به داشبورد
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">
              <FileText className="h-8 w-8 inline mr-2" />
              خدمات تایپ
            </h1>
            <p className="text-gray-300">
              سفارش تایپ متن، تبدیل فایل و خدمات تایپ تخصصی
            </p>
          </div>
        </div>
      </div>

      {/* Form */}
      <div className="max-w-2xl mx-auto">
        <GlowCard glowColor="purple" size="lg">
          <Card className="bg-white/10 border-white/20">
            <CardHeader>
              <CardTitle className="text-white text-2xl font-bold text-center">
                ایجاد سفارش تایپ جدید
              </CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Customer Info */}
                <div>
                  <h3 className="text-lg font-semibold text-white mb-4">اطلاعات مشتری</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-white mb-2">نام کامل</label>
                      <Input
                        name="user_name"
                        value={formData.user_name}
                        onChange={handleChange}
                        required
                        className="bg-white/10 border-white/20 text-white"
                        placeholder="نام و نام خانوادگی"
                      />
                    </div>
                    <div>
                      <label className="block text-white mb-2">شماره تماس</label>
                      <Input
                        name="user_phone"
                        value={formData.user_phone}
                        onChange={handleChange}
                        required
                        type="tel"
                        className="bg-white/10 border-white/20 text-white"
                        placeholder="09123456789"
                      />
                    </div>
                    <div className="col-span-2">
                      <label className="block text-white mb-2">ایمیل (اختیاری)</label>
                      <Input
                        name="user_email"
                        value={formData.user_email}
                        onChange={handleChange}
                        type="email"
                        className="bg-white/10 border-white/20 text-white"
                        placeholder="example@email.com"
                      />
                    </div>
                  </div>
                </div>

                {/* File Upload Section */}
                <div>
                  <h3 className="text-lg font-semibold text-white mb-4">
                    <Upload className="h-5 w-5 inline mr-2" />
                    بارگذاری فایل
                  </h3>
                  
                  <div
                    className={`border-2 border-dashed rounded-lg p-6 text-center transition-all duration-200 cursor-pointer ${
                      dragActive 
                        ? 'border-purple-400 bg-purple-400/10' 
                        : formData.document_file 
                        ? 'border-green-400 bg-green-400/10'
                        : 'border-white/20 bg-white/5 hover:border-white/40 hover:bg-white/10'
                    }`}
                    onDragEnter={handleDrag}
                    onDragOver={handleDrag}
                    onDragLeave={handleDrag}
                    onDrop={handleDrop}
                    onClick={() => fileInputRef.current?.click()}
                  >
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept=".doc,.docx,.pdf,.txt"
                      onChange={(e) => handleFileSelect(e.target.files)}
                      className="hidden"
                    />
                    
                    {formData.document_file ? (
                      <div className="text-green-400">
                        <FileText className="h-12 w-12 mx-auto mb-2" />
                        <p className="font-medium">{formData.document_file.name}</p>
                        <p className="text-sm text-gray-300 mt-1">
                          {formatFileSize(formData.document_file.size)}
                        </p>
                        <Button
                          type="button"
                          variant="outline"
                          size="sm"
                          className="mt-3 border-white/20 text-white hover:bg-white/10"
                          onClick={(e) => {
                            e.stopPropagation();
                            setFormData(prev => ({ ...prev, document_file: null }));
                          }}
                        >
                          حذف فایل
                        </Button>
                      </div>
                    ) : (
                      <div className="text-white">
                        <Upload className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                        <p className="text-lg font-medium mb-2">
                          فایل خود را اینجا بکشید و رها کنید
                        </p>
                        <p className="text-gray-300 mb-4">یا کلیک کنید تا فایل انتخاب کنید</p>
                        <p className="text-sm text-gray-400">
                          فرمت‌های مجاز: DOC, DOCX, PDF, TXT - حداکثر 10MB
                        </p>
                      </div>
                    )}
                  </div>
                </div>

                {/* Typing Options */}
                <div>
                  <h3 className="text-lg font-semibold text-white mb-4">
                    <Calculator className="h-5 w-5 inline mr-2" />
                    گزینه‌های تایپ
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-white mb-2">تعداد صفحات</label>
                      <div className="flex items-center space-x-2 space-x-reverse">
                        <Button
                          type="button"
                          variant="outline"
                          size="sm"
                          className="border-white/20 text-white hover:bg-white/10"
                          onClick={() => setFormData(prev => ({ ...prev, page_count: Math.max(1, prev.page_count - 1) }))}
                        >
                          <Minus className="h-4 w-4" />
                        </Button>
                        <Input
                          name="page_count"
                          type="number"
                          min={1}
                          value={formData.page_count}
                          onChange={handleChange}
                          required
                          className="bg-white/10 border-white/20 text-white text-center"
                        />
                        <Button
                          type="button"
                          variant="outline"
                          size="sm"
                          className="border-white/20 text-white hover:bg-white/10"
                          onClick={() => setFormData(prev => ({ ...prev, page_count: prev.page_count + 1 }))}
                        >
                          <Plus className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                    <div>
                      <label className="block text-white mb-2">نحوه تحویل</label>
                      <select
                        name="delivery_option"
                        value={formData.delivery_option}
                        onChange={handleChange}
                        className="w-full p-2 rounded bg-white/10 border border-white/20 text-white"
                      >
                        <option value="email">ارسال از طریق ایمیل</option>
                        <option value="print">چاپ توسط کارکنان</option>
                      </select>
                    </div>
                  </div>
                  <div className="mt-4">
                    <label className="block text-white mb-2">توضیحات (اختیاری)</label>
                    <textarea
                      name="description"
                      value={formData.description}
                      onChange={handleChange}
                      rows={3}
                      className="w-full p-2 rounded bg-white/10 border border-white/20 text-white placeholder:text-gray-400"
                      placeholder="توضیحات اضافی برای سفارش..."
                    />
                  </div>
                </div>

                {/* Accessories */}
                <div>
                  <h3 className="text-lg font-semibold text-white mb-4">لوازم جانبی و تکمیلی</h3>
                  {loadingAccessories ? (
                    <div className="text-gray-300">در حال بارگذاری لوازم جانبی...</div>
                  ) : Object.keys(accessories).length === 0 ? (
                    <div className="text-gray-300">لوازم جانبی‌ای موجود نیست</div>
                  ) : (
                    Object.entries(accessories).map(([category, items]: any) => (
                      <div key={category} className="mb-6">
                        <h4 className="text-white font-bold mb-3 text-base">{category}</h4>
                        <div className="grid grid-cols-1 gap-4">
                          {items.map((accessory: any) => {
                            const selectedAccessory = formData.accessories.find(a => a.id === accessory.id);
                            const isSelected = !!selectedAccessory;
                            
                            return (
                              <div key={accessory.id} className={`bg-white/5 rounded-lg p-4 border-2 transition-all duration-200 ${
                                isSelected ? 'border-purple-400/50 bg-purple-400/10' : 'border-white/10 hover:border-white/20'
                              }`}>
                                <label className="flex items-start gap-3 cursor-pointer">
                                  <input
                                    type="checkbox"
                                    checked={isSelected}
                                    onChange={(e) => handleAccessory(accessory.id, e.target.checked, accessory.base_price)}
                                    className="rounded mt-1 accent-purple-500"
                                  />
                                  <div className="flex-1 min-w-0">
                                    <div className="flex justify-between items-start mb-2 gap-2">
                                      <span className="text-white font-medium text-sm leading-tight">{accessory.name}</span>
                                      <span className="text-green-400 font-medium text-sm whitespace-nowrap">
                                        +{accessory.base_price.toLocaleString()} تومان
                                      </span>
                                    </div>
                                    {accessory.description && (
                                      <div className="text-xs text-gray-300 mb-3 leading-relaxed">{accessory.description}</div>
                                    )}
                                    
                                    {isSelected && (
                                      <div className="flex items-center gap-3 mt-3 p-2 bg-white/5 rounded border border-white/10">
                                        <span className="text-white text-sm font-medium">تعداد:</span>
                                        <div className="flex items-center gap-2">
                                          <Button
                                            type="button"
                                            variant="outline"
                                            size="sm"
                                            className="border-white/20 text-white hover:bg-white/10 h-7 w-7 p-0 flex items-center justify-center"
                                            onClick={() => handleAccessoryQuantity(accessory.id, -1)}
                                          >
                                            <Minus className="h-3 w-3" />
                                          </Button>
                                          <span className="bg-white/10 px-3 py-1 rounded text-white min-w-[2.5rem] text-center text-sm font-medium">
                                            {selectedAccessory?.quantity || 1}
                                          </span>
                                          <Button
                                            type="button"
                                            variant="outline"
                                            size="sm"
                                            className="border-white/20 text-white hover:bg-white/10 h-7 w-7 p-0 flex items-center justify-center"
                                            onClick={() => handleAccessoryQuantity(accessory.id, 1)}
                                          >
                                            <Plus className="h-3 w-3" />
                                          </Button>
                                        </div>
                                        <span className="text-green-400 text-sm font-medium">
                                          = {((selectedAccessory?.quantity || 1) * accessory.base_price).toLocaleString()} تومان
                                        </span>
                                      </div>
                                    )}
                                  </div>
                                </label>
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    ))
                  )}
                </div>

                {/* Price Summary */}
                <div className="bg-gradient-to-r from-white/10 to-white/5 rounded-lg p-5 border border-white/20">
                  <h4 className="text-white font-bold mb-3 text-lg">خلاصه هزینه</h4>
                  <div className="space-y-2 text-gray-300">
                    <div className="flex justify-between items-center">
                      <span>قیمت پایه هر صفحه:</span>
                      <span className="font-medium">{(100000).toLocaleString()} تومان</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>تعداد صفحات:</span>
                      <span className="font-medium">{formData.page_count}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>هزینه تایپ:</span>
                      <span className="font-medium">{(100000 * formData.page_count).toLocaleString()} تومان</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>لوازم جانبی:</span>
                      <span className="font-medium">{formData.accessories.reduce((sum, a) => sum + (a.price * a.quantity), 0).toLocaleString()} تومان</span>
                    </div>
                  </div>
                  <div className="mt-4 pt-3 border-t border-white/20">
                    <div className="flex justify-between items-center">
                      <span className="text-xl font-bold text-white">جمع کل:</span>
                      <span className="text-2xl font-bold text-green-400">
                        {calculatePrice().toLocaleString()} تومان
                      </span>
                    </div>
                  </div>
                </div>

                {/* Messages */}
                {error && (
                  <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-lg">
                    <div className="font-medium">{error}</div>
                  </div>
                )}
                {success && (
                  <div className="bg-green-500/10 border border-green-500/30 text-green-400 p-4 rounded-lg">
                    <div className="font-medium">{success}</div>
                  </div>
                )}

                {/* Submit Button */}
                <Button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-bold py-4 text-lg rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl"
                >
                  {loading ? 'در حال ثبت سفارش...' : 'ثبت سفارش تایپ'}
                </Button>
              </form>
            </CardContent>
          </Card>
        </GlowCard>
      </div>
    </div>
  );
}

export default function TypingServicePage() {
  return (
    <ProtectedRoute>
      <TypingServiceContent />
    </ProtectedRoute>
  );
}
