'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { digitalShopAPI } from '@/lib/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import ProtectedRoute from '@/components/ProtectedRoute';
import { 
  ArrowLeft,
  Package,
  Clock,
  CheckCircle,
  XCircle,
  Truck,
  CreditCard
} from 'lucide-react';
import Link from 'next/link';

interface OrderItem {
  id: number;
  product: {
    id: number;
    name: string;
    price: number;
    image: string;
  };
  quantity: number;
  total_price: number;
}

interface Order {
  id: number;
  order_number: string;
  status: string;
  payment_status: string;
  total_amount: number;
  created_at: string;
  items: OrderItem[];
  customer_name: string;
  customer_phone: string;
  customer_address: string;
  customer_notes?: string;
}

function ShopOrdersContent() {
  const { user } = useAuth();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      
      // Try API first
      try {
        const response = await digitalShopAPI.getDigitalShopOrders();
        if (response && response.success && Array.isArray(response.orders) && response.orders.length > 0) {
          setOrders(response.orders);
        } else {
          // Fallback to local orders if API returns empty/unauthorized
          const localOrders = JSON.parse(localStorage.getItem('orders') || '[]');
          setOrders(Array.isArray(localOrders) ? localOrders : []);
        }
      } catch (apiError) {
        // If API fails, get orders from localStorage
        const localOrders = JSON.parse(localStorage.getItem('orders') || '[]');
        setOrders(Array.isArray(localOrders) ? localOrders : []);
      }
    } catch (error) {
      console.error('Error fetching orders:', error);
      // Use localStorage orders as fallback
      const localOrders = JSON.parse(localStorage.getItem('orders') || '[]');
      setOrders(localOrders);
    } finally {
      setLoading(false);
    }
  };

  const getStatusInfo = (status: string) => {
    switch (status) {
      case 'pending':
        return {
          label: 'در انتظار تایید',
          icon: Clock,
          color: 'text-yellow-400',
          bgColor: 'bg-yellow-400/20',
          borderColor: 'border-yellow-400/30'
        };
      case 'pending_payment':
        return {
          label: 'در انتظار پرداخت',
          icon: CreditCard,
          color: 'text-orange-400',
          bgColor: 'bg-orange-400/20',
          borderColor: 'border-orange-400/30'
        };
      case 'confirmed':
        return {
          label: 'تایید شده',
          icon: CheckCircle,
          color: 'text-green-400',
          bgColor: 'bg-green-400/20',
          borderColor: 'border-green-400/30'
        };
      case 'processing':
        return {
          label: 'در حال پردازش',
          icon: Package,
          color: 'text-blue-400',
          bgColor: 'bg-blue-400/20',
          borderColor: 'border-blue-400/30'
        };
      case 'shipped':
        return {
          label: 'ارسال شده',
          icon: Truck,
          color: 'text-purple-400',
          bgColor: 'bg-purple-400/20',
          borderColor: 'border-purple-400/30'
        };
      case 'delivered':
        return {
          label: 'تحویل داده شده',
          icon: CheckCircle,
          color: 'text-green-400',
          bgColor: 'bg-green-400/20',
          borderColor: 'border-green-400/30'
        };
      case 'cancelled':
        return {
          label: 'لغو شده',
          icon: XCircle,
          color: 'text-red-400',
          bgColor: 'bg-red-400/20',
          borderColor: 'border-red-400/30'
        };
      default:
        return {
          label: 'نامشخص',
          icon: Package,
          color: 'text-gray-400',
          bgColor: 'bg-gray-400/20',
          borderColor: 'border-gray-400/30'
        };
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('fa-IR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="text-white text-xl">در حال بارگذاری...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <Link href="/shop">
            <Button variant="outline" className="border-white/20 text-white hover:bg-white/10">
              <ArrowLeft className="h-4 w-4 mr-2" />
              بازگشت به فروشگاه
            </Button>
          </Link>
          <h1 className="text-3xl font-bold text-white">سفارشات من</h1>
        </div>

        {orders.length === 0 ? (
          <Card className="bg-white/10 border-white/20">
            <CardContent className="p-12 text-center">
              <Package className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-white mb-2">هنوز سفارشی ثبت نکرده‌اید</h3>
              <p className="text-gray-300 mb-6">برای مشاهده سفارشات، ابتدا محصولی خریداری کنید</p>
              <Link href="/shop">
                <Button className="bg-orange-600 hover:bg-orange-700 text-white">
                  <Package className="h-4 w-4 mr-2" />
                  مشاهده محصولات
                </Button>
              </Link>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-6">
            {orders.map((order) => {
              const statusInfo = getStatusInfo(order.status);
              const StatusIcon = statusInfo.icon;
              
              return (
                <Card key={order.id} className="bg-white/10 border-white/20">
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle className="text-white">سفارش {order.order_number}</CardTitle>
                        <CardDescription className="text-gray-300">
                          ثبت شده در {formatDate(order.created_at)}
                        </CardDescription>
                      </div>
                      <div className={`px-3 py-1 rounded-full ${statusInfo.bgColor} ${statusInfo.borderColor} border`}>
                        <div className="flex items-center gap-2">
                          <StatusIcon className={`h-4 w-4 ${statusInfo.color}`} />
                          <span className={`text-sm font-medium ${statusInfo.color}`}>
                            {statusInfo.label}
                          </span>
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    {/* Order Items */}
                    <div className="space-y-3 mb-6">
                      {order.items.map((item) => (
                        <div key={item.id} className="flex items-center gap-3 p-3 bg-white/5 rounded-lg">
                          <div className="w-12 h-12 bg-white/10 rounded-lg flex items-center justify-center overflow-hidden">
                            {item.product.image ? (
                              <img
                                src={item.product.image}
                                alt={item.product.name}
                                className="w-full h-full object-cover"
                              />
                            ) : (
                              <Package className="h-6 w-6 text-gray-400" />
                            )}
                          </div>
                          <div className="flex-1">
                            <h4 className="text-white font-medium">{item.product.name}</h4>
                            <p className="text-gray-400 text-sm">
                              {item.quantity} عدد × {item.product.price.toLocaleString()} تومان
                            </p>
                          </div>
                          <div className="text-right">
                            <p className="text-white font-semibold">
                              {item.total_price.toLocaleString()} تومان
                            </p>
                          </div>
                        </div>
                      ))}
                    </div>

                    {/* Order Details */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                      <div>
                        <h4 className="text-white font-semibold mb-2">اطلاعات مشتری</h4>
                        <div className="space-y-1 text-sm">
                          <p className="text-gray-300">
                            <span className="text-white">نام:</span> {order.customer_name}
                          </p>
                          <p className="text-gray-300">
                            <span className="text-white">تلفن:</span> {order.customer_phone}
                          </p>
                          <p className="text-gray-300">
                            <span className="text-white">آدرس:</span> {order.customer_address}
                          </p>
                          {order.customer_notes && (
                            <p className="text-gray-300">
                              <span className="text-white">یادداشت:</span> {order.customer_notes}
                            </p>
                          )}
                        </div>
                      </div>
                      
                      <div>
                        <h4 className="text-white font-semibold mb-2">جزئیات سفارش</h4>
                        <div className="space-y-1 text-sm">
                          <p className="text-gray-300">
                            <span className="text-white">شماره سفارش:</span> {order.order_number}
                          </p>
                          <p className="text-gray-300">
                            <span className="text-white">تاریخ ثبت:</span> {formatDate(order.created_at)}
                          </p>
                          <p className="text-gray-300">
                            <span className="text-white">وضعیت:</span> {statusInfo.label}
                          </p>
                          <p className="text-gray-300">
                            <span className="text-white">مبلغ کل:</span> {order.total_amount.toLocaleString()} تومان
                          </p>
                        </div>
                      </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex flex-wrap gap-3">
                      {order.status === 'pending_payment' && (
                        <Button className="bg-orange-600 hover:bg-orange-700 text-white">
                          <CreditCard className="h-4 w-4 mr-2" />
                          پرداخت سفارش
                        </Button>
                      )}
                      
                      {order.status === 'delivered' && (
                        <Button variant="outline" className="border-white/20 text-white hover:bg-white/10">
                          <Package className="h-4 w-4 mr-2" />
                          خرید مجدد
                        </Button>
                      )}
                      
                      <Button variant="outline" className="border-white/20 text-white hover:bg-white/10">
                        <Package className="h-4 w-4 mr-2" />
                        مشاهده جزئیات
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

export default function ShopOrdersPage() {
  return (
    <ProtectedRoute>
      <ShopOrdersContent />
    </ProtectedRoute>
  );
}