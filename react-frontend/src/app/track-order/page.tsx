'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import Link from 'next/link';
import { ArrowLeft, Search, FileText, Printer, Package, Clock, CheckCircle, AlertCircle } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function TrackOrderPage() {
  const [orderId, setOrderId] = useState('');
  const [email, setEmail] = useState('');
  const [orderData, setOrderData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [serviceType, setServiceType] = useState<'typing' | 'print'>('typing');

  const handleTrackOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setOrderData(null);

    try {
      const endpoint = serviceType === 'typing' 
        ? `http://127.0.0.1:8000/typing/track/?order_id=${orderId}&email=${email}`
        : `http://127.0.0.1:8000/print/track/?order_id=${orderId}&email=${email}`;

      const response = await fetch(endpoint, {
        credentials: 'include'
      });

      if (response.ok) {
        const data = await response.text();
        // Since the Django view returns HTML, we'll need to handle this differently
        // For now, let's try to get JSON data from the API endpoints instead
        const apiEndpoint = serviceType === 'typing'
          ? `http://127.0.0.1:8000/typing/api/orders/?email=${email}`
          : `http://127.0.0.1:8000/print/api/my-orders/?email=${email}`;

        const apiResponse = await fetch(apiEndpoint, {
          credentials: 'include'
        });

        const apiResult = await apiResponse.json();

        if (apiResult.success) {
          const order = apiResult.orders.find((o: any) => o.id.toString() === orderId);
          if (order) {
            setOrderData(order);
          } else {
            setError('سفارش با شماره و ایمیل مشخص شده یافت نشد');
          }
        } else {
          setError(apiResult.message || 'خطا در یافتن سفارش');
        }
      } else {
        setError('سفارش یافت نشد. لطفاً شماره سفارش و ایمیل را بررسی کنید.');
      }
    } catch (err) {
      setError('خطا در ارتباط با سرور. لطفاً مجدداً تلاش کنید.');
      console.error('Tracking error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      'pending_review': 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20',
      'awaiting_payment': 'bg-orange-500/10 text-orange-500 border-orange-500/20',
      'awaiting_approval': 'bg-blue-500/10 text-blue-500 border-blue-500/20',
      'in_progress': 'bg-purple-500/10 text-purple-500 border-purple-500/20',
      'awaiting_final_approval': 'bg-green-500/10 text-green-500 border-green-500/20',
      'completed': 'bg-gray-500/10 text-gray-500 border-gray-500/20',
      'printing': 'bg-blue-500/10 text-blue-500 border-blue-500/20',
      'ready': 'bg-green-500/10 text-green-500 border-green-500/20',
      'rejected': 'bg-red-500/10 text-red-500 border-red-500/20',
    };
    return colors[status] || 'bg-gray-500/10 text-gray-500 border-gray-500/20';
  };

  const getStatusText = (status: string) => {
    const statusTexts: Record<string, string> = {
      'pending_review': 'در انتظار بررسی',
      'awaiting_payment': 'در انتظار پرداخت',
      'awaiting_approval': 'در انتظار تایید',
      'in_progress': 'در حال انجام',
      'awaiting_final_approval': 'در انتظار تایید نهایی',
      'completed': 'تکمیل شده',
      'printing': 'در حال چاپ',
      'ready': 'آماده تحویل',
      'rejected': 'رد شده',
    };
    return statusTexts[status] || status;
  };

  const getStatusIcon = (status: string) => {
    const icons: Record<string, React.ReactNode> = {
      'pending_review': <Clock className="h-4 w-4" />,
      'awaiting_payment': <Package className="h-4 w-4" />,
      'awaiting_approval': <Clock className="h-4 w-4" />,
      'in_progress': <FileText className="h-4 w-4" />,
      'printing': <Printer className="h-4 w-4" />,
      'awaiting_final_approval': <Package className="h-4 w-4" />,
      'completed': <CheckCircle className="h-4 w-4" />,
      'ready': <CheckCircle className="h-4 w-4" />,
      'rejected': <AlertCircle className="h-4 w-4" />,
    };
    return icons[status] || <Clock className="h-4 w-4" />;
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
              <Search className="h-8 w-8 inline mr-2" />
              پیگیری سفارش
            </h1>
            <p className="text-gray-300">
              با وارد کردن شماره سفارش و ایمیل، وضعیت سفارش خود را پیگیری کنید
            </p>
          </div>
        </div>
      </div>

      {/* Search Form */}
      <div className="max-w-4xl mx-auto mb-8">
        <Card className="bg-white/10 border-white/20">
          <CardHeader>
            <CardTitle className="text-white text-center">جستجوی سفارش</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleTrackOrder} className="space-y-6">
              {/* Service Type Selection */}
              <div className="flex gap-4 justify-center mb-6">
                <Button
                  type="button"
                  onClick={() => setServiceType('typing')}
                  className={`flex-1 ${serviceType === 'typing' 
                    ? 'bg-purple-600 hover:bg-purple-700' 
                    : 'bg-gray-600 hover:bg-gray-700'
                  }`}
                >
                  <FileText className="h-4 w-4 mr-2" />
                  سفارش تایپ
                </Button>
                <Button
                  type="button"
                  onClick={() => setServiceType('print')}
                  className={`flex-1 ${serviceType === 'print' 
                    ? 'bg-green-600 hover:bg-green-700' 
                    : 'bg-gray-600 hover:bg-gray-700'
                  }`}
                >
                  <Printer className="h-4 w-4 mr-2" />
                  سفارش چاپ
                </Button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="orderId" className="text-white">شماره سفارش</Label>
                  <Input
                    id="orderId"
                    type="number"
                    value={orderId}
                    onChange={(e) => setOrderId(e.target.value)}
                    placeholder="مثال: 123"
                    className="bg-white/10 border-white/20 text-white placeholder-gray-400"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="email" className="text-white">ایمیل</Label>
                  <Input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="example@email.com"
                    className="bg-white/10 border-white/20 text-white placeholder-gray-400"
                    required
                  />
                </div>
              </div>

              <Button 
                type="submit" 
                disabled={loading}
                className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
              >
                {loading ? 'در حال جستجو...' : 'پیگیری سفارش'}
                <Search className="h-4 w-4 mr-2" />
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>

      {/* Error Message */}
      {error && (
        <div className="max-w-4xl mx-auto mb-8">
          <Card className="bg-red-500/10 border-red-500/20">
            <CardContent className="p-6 text-center">
              <AlertCircle className="h-12 w-12 text-red-400 mx-auto mb-4" />
              <div className="text-red-400 text-lg">{error}</div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Order Details */}
      {orderData && (
        <div className="max-w-4xl mx-auto">
          <Card className="bg-white/10 border-white/20">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-white flex items-center gap-2">
                  {serviceType === 'typing' ? (
                    <FileText className="h-6 w-6" />
                  ) : (
                    <Printer className="h-6 w-6" />
                  )}
                  سفارش {serviceType === 'typing' ? 'تایپ' : 'چاپ'} #{orderData.id}
                </CardTitle>
                <Badge className={`${getStatusColor(orderData.status)} flex items-center gap-1`}>
                  {getStatusIcon(orderData.status)}
                  {getStatusText(orderData.status)}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Customer Information */}
              <div>
                <h3 className="text-lg font-semibold text-white mb-3">اطلاعات مشتری</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-white">
                  <div>
                    <span className="text-gray-400">نام:</span>
                    <div>{orderData.user_name}</div>
                  </div>
                  <div>
                    <span className="text-gray-400">ایمیل:</span>
                    <div>{orderData.user_email || email}</div>
                  </div>
                  <div>
                    <span className="text-gray-400">تلفن:</span>
                    <div>{orderData.user_phone}</div>
                  </div>
                </div>
              </div>

              {/* Order Details */}
              <div>
                <h3 className="text-lg font-semibold text-white mb-3">جزئیات سفارش</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-white">
                  {serviceType === 'typing' ? (
                    <>
                      <div>
                        <span className="text-gray-400">تعداد صفحات:</span>
                        <div>{orderData.page_count}</div>
                      </div>
                      <div>
                        <span className="text-gray-400">نحوه تحویل:</span>
                        <div>{orderData.delivery_option === 'email' ? 'ایمیل' : 'چاپ'}</div>
                      </div>
                    </>
                  ) : (
                    <>
                      <div>
                        <span className="text-gray-400">تعداد کپی:</span>
                        <div>{orderData.copies}</div>
                      </div>
                      <div>
                        <span className="text-gray-400">نوع کاغذ:</span>
                        <div>{orderData.paper_type}</div>
                      </div>
                    </>
                  )}
                  <div>
                    <span className="text-gray-400">تاریخ ایجاد:</span>
                    <div>{new Date(orderData.created_at).toLocaleDateString('fa-IR')}</div>
                  </div>
                  <div>
                    <span className="text-gray-400">مبلغ کل:</span>
                    <div className="text-green-400 font-bold">
                      {orderData.total_price?.toLocaleString() || '0'} تومان
                    </div>
                  </div>
                </div>
              </div>

              {/* Description */}
              {orderData.description && (
                <div>
                  <h3 className="text-lg font-semibold text-white mb-3">توضیحات</h3>
                  <div className="bg-white/5 rounded p-3 text-white">
                    {orderData.description}
                  </div>
                </div>
              )}

              {/* Accessories */}
              {orderData.accessories && orderData.accessories.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold text-white mb-3">لوازم جانبی</h3>
                  <div className="space-y-2">
                    {orderData.accessories.map((acc: any, index: number) => (
                      <div key={index} className="bg-white/5 rounded p-3 text-white flex justify-between">
                        <span>{acc.name} (تعداد: {acc.quantity})</span>
                        <span>{acc.price.toLocaleString()} تومان</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Actions */}
              <div className="flex gap-3 pt-4 border-t border-white/20">
                <Link 
                  href={serviceType === 'typing' ? '/typing-orders' : '/print-orders'}
                  className="flex-1"
                >
                  <Button className="w-full bg-blue-600 hover:bg-blue-700">
                    مشاهده همه سفارشات
                  </Button>
                </Link>
                {orderData.status === 'awaiting_payment' && (
                  <Button className="flex-1 bg-green-600 hover:bg-green-700">
                    پرداخت
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
