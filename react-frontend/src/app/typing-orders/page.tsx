'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/contexts/AuthContext';
import ProtectedRoute from '@/components/ProtectedRoute';
import Link from 'next/link';
import { ArrowLeft, FileText, Package, Clock, CheckCircle } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

function TypingOrdersContent() {
  const { user } = useAuth();
  const [orders, setOrders] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (user?.email) {
      fetchOrders();
    }
  }, [user]);

  const fetchOrders = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/typing/api/orders/?email=${user?.email}`, {
        credentials: 'include'
      });
      const result = await response.json();

      if (result.success) {
        setOrders(result.orders);
      } else {
        setError(result.message || 'خطا در دریافت سفارشات');
      }
    } catch (err) {
      setError('خطا در ارتباط با سرور');
      console.error('Error fetching orders:', err);
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
      'rejected': 'bg-red-500/10 text-red-500 border-red-500/20',
      'cancelled': 'bg-gray-500/10 text-gray-500 border-gray-500/20',
    };
    return colors[status] || 'bg-gray-500/10 text-gray-500 border-gray-500/20';
  };

  const getStatusText = (status: string) => {
    const statusTexts: Record<string, string> = {
      'pending_review': 'در انتظار بررسی',
      'awaiting_payment': 'در انتظار پرداخت',
      'awaiting_approval': 'در انتظار تایید',
      'in_progress': 'در حال تایپ',
      'awaiting_final_approval': 'در انتظار تایید نهایی',
      'completed': 'تکمیل شده',
      'rejected': 'رد شده',
      'cancelled': 'لغو شده',
    };
    return statusTexts[status] || status;
  };

  const getStatusIcon = (status: string) => {
    const icons: Record<string, React.ReactNode> = {
      'pending_review': <Clock className="h-4 w-4" />,
      'awaiting_payment': <Package className="h-4 w-4" />,
      'awaiting_approval': <Clock className="h-4 w-4" />,
      'in_progress': <FileText className="h-4 w-4" />,
      'awaiting_final_approval': <Package className="h-4 w-4" />,
      'completed': <CheckCircle className="h-4 w-4" />,
    };
    return icons[status] || <Clock className="h-4 w-4" />;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6 flex items-center justify-center">
        <div className="text-white text-xl">در حال بارگذاری سفارشات...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
      {/* Header */}
      <div className="max-w-6xl mx-auto mb-8">
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
              سفارشات تایپ من
            </h1>
            <p className="text-gray-300">
              مشاهده و پیگیری سفارشات تایپ شما
            </p>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-6xl mx-auto">
        {error ? (
          <Card className="bg-red-500/10 border-red-500/20">
            <CardContent className="p-6 text-center">
              <div className="text-red-400 text-lg mb-4">{error}</div>
              <Button 
                onClick={fetchOrders}
                className="bg-red-600 hover:bg-red-700 text-white"
              >
                تلاش مجدد
              </Button>
            </CardContent>
          </Card>
        ) : orders.length === 0 ? (
          <Card className="bg-white/10 border-white/20">
            <CardContent className="p-8 text-center">
              <FileText className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h2 className="text-xl font-bold text-white mb-2">هیچ سفارشی یافت نشد</h2>
              <p className="text-gray-300 mb-6">
                شما هنوز هیچ سفارش تایپی ندارید
              </p>
              <Link href="/typing-service">
                <Button className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700">
                  ایجاد سفارش جدید
                </Button>
              </Link>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-6">
            {orders.map((order) => (
              <Card key={order.id} className="bg-white/10 border-white/20 hover:bg-white/15 transition-colors">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-white flex items-center gap-2">
                      <FileText className="h-5 w-5" />
                      سفارش تایپ #{order.id}
                    </CardTitle>
                    <Badge className={`${getStatusColor(order.status)} flex items-center gap-1`}>
                      {getStatusIcon(order.status)}
                      {getStatusText(order.status)}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-white">
                    <div>
                      <div className="text-sm text-gray-400">اطلاعات سفارش</div>
                      <div className="mt-1">
                        <div>تعداد صفحات: {order.page_count}</div>
                        <div>نحوه تحویل: {order.delivery_option === 'email' ? 'ایمیل' : 'چاپ'}</div>
                        {order.description && (
                          <div className="text-sm mt-2">
                            <span className="text-gray-400">توضیحات:</span>
                            <div className="bg-white/5 rounded p-2 mt-1 text-xs">
                              {order.description}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>

                    <div>
                      <div className="text-sm text-gray-400">اطلاعات تماس</div>
                      <div className="mt-1">
                        <div>نام: {order.user_name}</div>
                        <div>تلفن: {order.user_phone}</div>
                        <div>ایمیل: {order.user_email}</div>
                      </div>
                    </div>

                    <div>
                      <div className="text-sm text-gray-400">جزئیات مالی</div>
                      <div className="mt-1">
                        <div>قیمت پایه: {(100000 * order.page_count).toLocaleString()} تومان</div>
                        {order.accessories && order.accessories.length > 0 && (
                          <div>لوازم جانبی: {order.accessories.reduce((sum: number, acc: any) => sum + acc.price, 0).toLocaleString()} تومان</div>
                        )}
                        <div className="text-green-400 font-bold">
                          مبلغ کل: {order.total_price?.toLocaleString() || (100000 * order.page_count + (order.accessories?.reduce((sum: number, acc: any) => sum + acc.price, 0) || 0)).toLocaleString()} تومان
                        </div>
                      </div>
                    </div>
                  </div>

                  {order.accessories && order.accessories.length > 0 && (
                    <div className="mt-4">
                      <div className="text-sm text-gray-400 mb-2">لوازم جانبی</div>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                        {order.accessories.map((acc: any, index: number) => (
                          <div key={index} className="bg-white/5 rounded p-2 text-white text-sm">
                            {acc.name} (تعداد: {acc.quantity}) - {acc.price.toLocaleString()} تومان
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="mt-4 pt-4 border-t border-white/20 flex items-center justify-between">
                    <div className="text-sm text-gray-400">
                      تاریخ ایجاد: {new Date(order.created_at).toLocaleDateString('fa-IR')}
                    </div>
                    <div className="flex gap-2">
                      <Button 
                        variant="outline" 
                        size="sm"
                        className="border-white/20 text-white hover:bg-white/10"
                      >
                        مشاهده جزئیات
                      </Button>
                      {order.status === 'awaiting_payment' && (
                        <Button 
                          size="sm"
                          className="bg-green-600 hover:bg-green-700 text-white"
                        >
                          پرداخت
                        </Button>
                      )}
                      {order.status === 'awaiting_final_approval' && (
                        <Button 
                          size="sm"
                          className="bg-blue-600 hover:bg-blue-700 text-white"
                        >
                          تایید نهایی
                        </Button>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default function TypingOrdersPage() {
  return (
    <ProtectedRoute>
      <TypingOrdersContent />
    </ProtectedRoute>
  );
}
