'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import ProtectedRoute from '@/components/ProtectedRoute';
import Link from 'next/link';
import { ArrowLeft, Printer } from 'lucide-react';
import { GlowCard } from '@/components/ui/spotlight-card';

function PrintServiceContent() {
  const { user } = useAuth();
  const router = useRouter();
  const [formData, setFormData] = useState({
    pages: 1,
    copies: 1,
    paper_size: 'A4',
    color_type: 'black_white',
    double_sided: false,
    phone: '',
    notes: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e: any) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const orderData = {
        email: user?.email || '',
        phone: formData.phone,
        pages: parseInt(formData.pages.toString()),
        copies: parseInt(formData.copies.toString()),
        paper_size: formData.paper_size,
        color_type: formData.color_type,
        double_sided: formData.double_sided,
        notes: formData.notes
      };

      const response = await fetch('http://127.0.0.1:8000/print/api/create/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(orderData)
      });

      const result = await response.json();

      if (result.success) {
        setSuccess('سفارش چاپ با موفقیت ثبت شد!');
        setTimeout(() => {
          router.push('/print-orders');
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

  const calculatePrice = () => {
    let basePrice = 5000;
    if (formData.color_type === 'color') basePrice *= 2;
    if (formData.double_sided) basePrice += 1000;
    return basePrice * formData.pages * formData.copies;
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
              <Printer className="h-8 w-8 inline mr-2" />
              خدمات چاپ
            </h1>
            <p className="text-gray-300">
              سفارش چاپ اسناد، تصاویر و فایل‌های مختلف با کیفیت بالا
            </p>
          </div>
        </div>
      </div>

      {/* Form */}
      <div className="max-w-2xl mx-auto">
        <GlowCard glowColor="green" size="lg">
          <Card className="bg-white/10 border-white/20">
            <CardHeader>
              <CardTitle className="text-white text-2xl font-bold text-center">
                ایجاد سفارش چاپ جدید
              </CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Print Details */}
                <div>
                  <h3 className="text-lg font-semibold text-white mb-4">جزئیات چاپ</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-white mb-2">تعداد صفحات</label>
                      <Input
                        type="number"
                        name="pages"
                        value={formData.pages}
                        onChange={handleChange}
                        min="1"
                        required
                        className="bg-white/10 border-white/20 text-white"
                      />
                    </div>
                    <div>
                      <label className="block text-white mb-2">تعداد نسخه</label>
                      <Input
                        type="number"
                        name="copies"
                        value={formData.copies}
                        onChange={handleChange}
                        min="1"
                        required
                        className="bg-white/10 border-white/20 text-white"
                      />
                    </div>
                    <div>
                      <label className="block text-white mb-2">اندازه کاغذ</label>
                      <select
                        name="paper_size"
                        value={formData.paper_size}
                        onChange={handleChange}
                        className="w-full p-2 rounded bg-white/10 border border-white/20 text-white"
                      >
                        <option value="A4">A4</option>
                        <option value="A3">A3</option>
                        <option value="A5">A5</option>
                        <option value="Letter">Letter</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-white mb-2">نوع چاپ</label>
                      <select
                        name="color_type"
                        value={formData.color_type}
                        onChange={handleChange}
                        className="w-full p-2 rounded bg-white/10 border border-white/20 text-white"
                      >
                        <option value="black_white">سیاه و سفید</option>
                        <option value="color">رنگی</option>
                      </select>
                    </div>
                  </div>
                  
                  <div className="mt-4">
                    <label className="flex items-center gap-2 text-white cursor-pointer">
                      <input
                        type="checkbox"
                        name="double_sided"
                        checked={formData.double_sided}
                        onChange={handleChange}
                        className="rounded"
                      />
                      چاپ دو طرفه
                    </label>
                  </div>
                </div>

                {/* Contact Info */}
                <div>
                  <h3 className="text-lg font-semibold text-white mb-4">اطلاعات تماس</h3>
                  <div className="grid grid-cols-1 gap-4">
                    <div>
                      <label className="block text-white mb-2">شماره تماس</label>
                      <Input
                        type="tel"
                        name="phone"
                        value={formData.phone}
                        onChange={handleChange}
                        required
                        placeholder="09123456789"
                        className="bg-white/10 border-white/20 text-white"
                      />
                    </div>
                  </div>
                </div>

                {/* Notes */}
                <div>
                  <label className="block text-white mb-2">توضیحات (اختیاری)</label>
                  <textarea
                    name="notes"
                    value={formData.notes}
                    onChange={handleChange}
                    rows={3}
                    className="w-full p-2 rounded bg-white/10 border border-white/20 text-white placeholder:text-gray-400"
                    placeholder="توضیحات اضافی برای سفارش..."
                  />
                </div>

                {/* Price Summary */}
                <div className="bg-white/5 rounded-lg p-4">
                  <h4 className="text-white font-bold mb-2">خلاصه هزینه</h4>
                  <div className="space-y-1 text-gray-300">
                    <div>قیمت پایه: {(5000).toLocaleString()} تومان</div>
                    <div>{formData.pages} صفحه × {formData.copies} نسخه</div>
                    {formData.color_type === 'color' && <div>چاپ رنگی: +100%</div>}
                    {formData.double_sided && <div>دو طرفه: +1000 تومان</div>}
                  </div>
                  <div className="mt-3 pt-3 border-t border-white/20">
                    <div className="text-xl font-bold text-white">
                      جمع کل: {calculatePrice().toLocaleString()} تومان
                    </div>
                  </div>
                </div>

                {/* Messages */}
                {error && (
                  <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-3 rounded">
                    {error}
                  </div>
                )}
                {success && (
                  <div className="bg-green-500/10 border border-green-500/20 text-green-400 p-3 rounded">
                    {success}
                  </div>
                )}

                {/* Submit Button */}
                <Button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white font-bold py-3"
                >
                  {loading ? 'در حال ثبت سفارش...' : 'ثبت سفارش چاپ'}
                </Button>
              </form>
            </CardContent>
          </Card>
        </GlowCard>
      </div>
    </div>
  );
}

export default function PrintServicePage() {
  return (
    <ProtectedRoute>
      <PrintServiceContent />
    </ProtectedRoute>
  );
}
