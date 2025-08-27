'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useState, useEffect } from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';
import AdminDashboardLayout from '@/components/admin/AdminDashboardLayout';

interface Order {
  id: number;
  orderNumber: string;
  customer: string;
  email: string;
  total: number;
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  orderDate: string;
  items: OrderItem[];
}

interface OrderItem {
  id: number;
  productName: string;
  quantity: number;
  price: number;
}

export default function ShopOrders() {
  const { user } = useAuth();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [showOrderDetails, setShowOrderDetails] = useState(false);

  useEffect(() => {
    // Simulate loading orders
    setTimeout(() => {
      setOrders([
        {
          id: 1,
          orderNumber: 'ORD-001',
          customer: 'علی احمدی',
          email: 'ali@example.com',
          total: 2750000,
          status: 'processing',
          orderDate: '2024-01-15',
          items: [
            { id: 1, productName: 'لپ‌تاپ ایسوس', quantity: 1, price: 25000000 },
            { id: 2, productName: 'هدفون سونی', quantity: 1, price: 2500000 }
          ]
        },
        {
          id: 2,
          orderNumber: 'ORD-002',
          customer: 'مریم رضایی',
          email: 'maryam@example.com',
          total: 450000,
          status: 'shipped',
          orderDate: '2024-01-14',
          items: [
            { id: 3, productName: 'موس گیمینگ', quantity: 1, price: 450000 }
          ]
        },
        {
          id: 3,
          orderNumber: 'ORD-003',
          customer: 'محمد کریمی',
          email: 'mohammad@example.com',
          total: 5000000,
          status: 'delivered',
          orderDate: '2024-01-13',
          items: [
            { id: 4, productName: 'هدفون سونی', quantity: 2, price: 2500000 }
          ]
        }
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'processing':
        return 'bg-blue-100 text-blue-800';
      case 'shipped':
        return 'bg-purple-100 text-purple-800';
      case 'delivered':
        return 'bg-green-100 text-green-800';
      case 'cancelled':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'pending':
        return 'در انتظار';
      case 'processing':
        return 'در حال پردازش';
      case 'shipped':
        return 'ارسال شده';
      case 'delivered':
        return 'تحویل داده شده';
      case 'cancelled':
        return 'لغو شده';
      default:
        return status;
    }
  };

  const updateOrderStatus = (orderId: number, newStatus: Order['status']) => {
    setOrders(orders.map(order => 
      order.id === orderId ? { ...order, status: newStatus } : order
    ));
  };

  const viewOrderDetails = (order: Order) => {
    setSelectedOrder(order);
    setShowOrderDetails(true);
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <AdminDashboardLayout>
          <div className="animate-pulse">Loading orders...</div>
        </AdminDashboardLayout>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <AdminDashboardLayout>
        <div className="p-6">
          <h1 className="text-3xl font-bold mb-8 text-gray-800">مدیریت سفارشات فروشگاه</h1>
          
          {/* Order Statistics */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-xl shadow-md p-6">
              <div className="text-2xl font-bold text-blue-600 mb-2">
                {orders.filter(o => o.status === 'pending').length}
              </div>
              <div className="text-sm text-gray-600">سفارشات در انتظار</div>
            </div>
            
            <div className="bg-white rounded-xl shadow-md p-6">
              <div className="text-2xl font-bold text-yellow-600 mb-2">
                {orders.filter(o => o.status === 'processing').length}
              </div>
              <div className="text-sm text-gray-600">در حال پردازش</div>
            </div>
            
            <div className="bg-white rounded-xl shadow-md p-6">
              <div className="text-2xl font-bold text-purple-600 mb-2">
                {orders.filter(o => o.status === 'shipped').length}
              </div>
              <div className="text-sm text-gray-600">ارسال شده</div>
            </div>
            
            <div className="bg-white rounded-xl shadow-md p-6">
              <div className="text-2xl font-bold text-green-600 mb-2">
                {orders.filter(o => o.status === 'delivered').length}
              </div>
              <div className="text-sm text-gray-600">تحویل داده شده</div>
            </div>
          </div>

          {/* Orders Table */}
          <div className="bg-white rounded-xl shadow-md">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      شماره سفارش
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      مشتری
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      مبلغ کل
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      وضعیت
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      تاریخ سفارش
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      عملیات
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {orders.map((order) => (
                    <tr key={order.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">{order.orderNumber}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">{order.customer}</div>
                        <div className="text-sm text-gray-500">{order.email}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {order.total.toLocaleString()} تومان
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <select
                          value={order.status}
                          onChange={(e) => updateOrderStatus(order.id, e.target.value as Order['status'])}
                          className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full border-none ${getStatusColor(order.status)}`}
                        >
                          <option value="pending">در انتظار</option>
                          <option value="processing">در حال پردازش</option>
                          <option value="shipped">ارسال شده</option>
                          <option value="delivered">تحویل داده شده</option>
                          <option value="cancelled">لغو شده</option>
                        </select>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {order.orderDate}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <button
                          onClick={() => viewOrderDetails(order)}
                          className="text-indigo-600 hover:text-indigo-900"
                        >
                          مشاهده جزئیات
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Order Details Modal */}
          {showOrderDetails && selectedOrder && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
              <div className="bg-white rounded-xl shadow-xl max-w-2xl w-full max-h-90vh overflow-y-auto">
                <div className="p-6">
                  <div className="flex justify-between items-center mb-6">
                    <h2 className="text-2xl font-bold text-gray-800">
                      جزئیات سفارش {selectedOrder.orderNumber}
                    </h2>
                    <button
                      onClick={() => setShowOrderDetails(false)}
                      className="text-gray-500 hover:text-gray-700"
                    >
                      ✕
                    </button>
                  </div>

                  <div className="grid grid-cols-2 gap-4 mb-6">
                    <div>
                      <h3 className="font-medium text-gray-700">مشتری</h3>
                      <p className="text-gray-900">{selectedOrder.customer}</p>
                      <p className="text-gray-600">{selectedOrder.email}</p>
                    </div>
                    <div>
                      <h3 className="font-medium text-gray-700">وضعیت</h3>
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(selectedOrder.status)}`}>
                        {getStatusText(selectedOrder.status)}
                      </span>
                    </div>
                  </div>

                  <div className="mb-6">
                    <h3 className="font-medium text-gray-700 mb-3">اقلام سفارش</h3>
                    <div className="space-y-2">
                      {selectedOrder.items.map((item) => (
                        <div key={item.id} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                          <div>
                            <div className="font-medium">{item.productName}</div>
                            <div className="text-sm text-gray-600">تعداد: {item.quantity}</div>
                          </div>
                          <div className="text-right">
                            <div className="font-medium">{(item.price * item.quantity).toLocaleString()} تومان</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="border-t pt-4">
                    <div className="flex justify-between items-center text-lg font-bold">
                      <span>مجموع:</span>
                      <span>{selectedOrder.total.toLocaleString()} تومان</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </AdminDashboardLayout>
    </ProtectedRoute>
  );
}
