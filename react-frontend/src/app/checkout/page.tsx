'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { digitalShopAPI } from '@/lib/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import ProtectedRoute from '@/components/ProtectedRoute';
import { 
  ArrowLeft,
  Package,
  CreditCard,
  User,
  Phone,
  MapPin,
  ShoppingCart
} from 'lucide-react';
import Link from 'next/link';
import { showToast } from '@/lib/utils';

interface CartItem {
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

interface Cart {
  items: CartItem[];
  total_items: number;
  total_price: number;
}

function CheckoutContent() {
  const { user } = useAuth();
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  
  // Form fields
  const [customerName, setCustomerName] = useState('');
  const [customerPhone, setCustomerPhone] = useState('');
  const [customerAddress, setCustomerAddress] = useState('');
  const [customerNotes, setCustomerNotes] = useState('');

  useEffect(() => {
    fetchCart();
    
    // Pre-fill customer name if available
    if (user?.first_name && user?.last_name) {
      setCustomerName(`${user.first_name} ${user.last_name}`);
    }
  }, [user]);

  const fetchCart = async () => {
    try {
      setLoading(true);
      // Read from canonical localStorage key (fallback to legacy)
      const raw = localStorage.getItem('shop_cart_items') || localStorage.getItem('cart') || '[]';
      const localCart = JSON.parse(raw);
      if (Array.isArray(localCart) && localCart.length > 0) {
        const totalPrice = localCart.reduce((sum: number, item: any) => sum + (item.price * item.quantity), 0);
        setCart({
          items: localCart.map((item: any) => ({
            id: item.id,
            product: {
              id: item.id,
              name: item.name,
              price: item.price,
              image: item.image
            },
            quantity: item.quantity,
            total_price: item.price * item.quantity
          })),
          total_items: localCart.reduce((sum: number, item: any) => sum + item.quantity, 0),
          total_price: totalPrice
        });
      } else {
        setCart({ items: [], total_items: 0, total_price: 0 });
      }
    } catch (error) {
      console.error('Error fetching cart:', error);
      setCart({ items: [], total_items: 0, total_price: 0 });
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!cart || cart.items.length === 0) {
      showToast('سبد خرید شما خالی است', 'error');
      return;
    }

    if (!customerName.trim() || !customerPhone.trim() || !customerAddress.trim()) {
      showToast('لطفاً تمام فیلدهای الزامی را پر کنید', 'error');
      return;
    }

    try {
      setSubmitting(true);
      
      // Create order via backend API
      const payload = {
        items: cart.items.map((it) => ({ product_id: it.product.id, quantity: it.quantity })),
        customer_name: customerName,
        customer_phone: customerPhone,
        customer_address: customerAddress,
        customer_notes: customerNotes,
      };
      const res = await digitalShopAPI.checkout(payload).catch(() => null);
      const hasApiOrder = res && res.success && res.order_id;
      const orderData = hasApiOrder ? {
        id: res.order_id,
        order_number: res.order_number,
        items: cart.items,
        total_amount: cart.total_price,
        customer_name: customerName,
        customer_phone: customerPhone,
        customer_address: customerAddress,
        customer_notes: customerNotes,
        status: 'pending_payment',
        created_at: new Date().toISOString()
      } : {
        // Fallback to local order if API fails (e.g., not logged in on backend)
        id: Date.now(),
        order_number: `ORD-${Date.now()}`,
        items: cart.items,
        total_amount: cart.total_price,
        customer_name: customerName,
        customer_phone: customerPhone,
        customer_address: customerAddress,
        customer_notes: customerNotes,
        status: 'pending_payment',
        created_at: new Date().toISOString()
      };
      // Save order locally for quick access and history
      const existingOrders = JSON.parse(localStorage.getItem('orders') || '[]');
      existingOrders.unshift(orderData);
      localStorage.setItem('orders', JSON.stringify(existingOrders));
      // Clear cart
      localStorage.removeItem('shop_cart_items');
      localStorage.removeItem('cart');
      localStorage.removeItem('cartCount');
      // For payment page
      localStorage.setItem('currentOrder', JSON.stringify(orderData));
      showToast(hasApiOrder ? 'سفارش شما با موفقیت ثبت شد! حالا به صفحه پرداخت منتقل می‌شوید.' : 'سفارش به صورت آفلاین ثبت شد؛ برای پرداخت ادامه دهید.', 'success');
      window.location.href = `/payment`;
    } catch (error) {
      console.error('Error submitting order:', error);
      // As a last resort: local fallback
      try {
        const orderData = {
          id: Date.now(),
          order_number: `ORD-${Date.now()}`,
          items: cart!.items,
          total_amount: cart!.total_price,
          customer_name: customerName,
          customer_phone: customerPhone,
          customer_address: customerAddress,
          customer_notes: customerNotes,
          status: 'pending_payment',
          created_at: new Date().toISOString()
        };
        const existingOrders = JSON.parse(localStorage.getItem('orders') || '[]');
        existingOrders.unshift(orderData);
        localStorage.setItem('orders', JSON.stringify(existingOrders));
        localStorage.setItem('currentOrder', JSON.stringify(orderData));
        localStorage.removeItem('shop_cart_items');
        localStorage.removeItem('cart');
        localStorage.removeItem('cartCount');
        showToast('سفارش به صورت آفلاین ثبت شد؛ برای پرداخت ادامه دهید.', 'success');
        window.location.href = `/payment`;
      } catch (e) {
        showToast('خطا در ثبت سفارش', 'error');
      }
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="text-white text-xl">در حال بارگذاری...</div>
      </div>
    );
  }

  if (!cart || cart.items.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center gap-4 mb-8">
            <Link href="/cart">
              <Button variant="outline" className="border-white/20 text-white hover:bg-white/10">
                <ArrowLeft className="h-4 w-4 mr-2" />
                بازگشت به سبد خرید
              </Button>
            </Link>
            <h1 className="text-3xl font-bold text-white">تکمیل خرید</h1>
          </div>

          <Card className="bg-white/10 border-white/20">
            <CardContent className="p-12 text-center">
              <ShoppingCart className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-white mb-2">سبد خرید شما خالی است</h3>
              <p className="text-gray-300 mb-6">برای تکمیل خرید ابتدا محصولی به سبد خرید اضافه کنید</p>
              <Link href="/shop">
                <Button className="bg-orange-600 hover:bg-orange-700 text-white">
                  <Package className="h-4 w-4 mr-2" />
                  مشاهده محصولات
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <Link href="/cart">
            <Button variant="outline" className="border-white/20 text-white hover:bg-white/10">
              <ArrowLeft className="h-4 w-4 mr-2" />
              بازگشت به سبد خرید
            </Button>
          </Link>
          <h1 className="text-3xl font-bold text-white">تکمیل خرید</h1>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Customer Information */}
            <div className="lg:col-span-2">
              <Card className="bg-white/10 border-white/20 mb-6">
                <CardHeader>
                  <CardTitle className="text-white">اطلاعات مشتری</CardTitle>
                  <CardDescription className="text-gray-300">
                    لطفاً اطلاعات خود را برای تکمیل سفارش وارد کنید
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label htmlFor="customerName" className="text-white">نام و نام خانوادگی <span className="text-red-400">*</span></Label>
                    <div className="relative">
                      <User className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                      <Input
                        id="customerName"
                        value={customerName}
                        onChange={(e) => setCustomerName(e.target.value)}
                        className="pl-10 bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                        placeholder="نام و نام خانوادگی خود را وارد کنید"
                        required
                      />
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="customerPhone" className="text-white">شماره تماس <span className="text-red-400">*</span></Label>
                    <div className="relative">
                      <Phone className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                      <Input
                        id="customerPhone"
                        value={customerPhone}
                        onChange={(e) => setCustomerPhone(e.target.value)}
                        className="pl-10 bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                        placeholder="شماره تماس خود را وارد کنید"
                        required
                      />
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="customerAddress" className="text-white">آدرس کامل <span className="text-red-400">*</span></Label>
                    <div className="relative">
                      <MapPin className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                      <Textarea
                        id="customerAddress"
                        value={customerAddress}
                        onChange={(e) => setCustomerAddress(e.target.value)}
                        className="pl-10 bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                        placeholder="آدرس کامل خود را وارد کنید"
                        rows={3}
                        required
                      />
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="customerNotes" className="text-white">یادداشت (اختیاری)</Label>
                    <Textarea
                      id="customerNotes"
                      value={customerNotes}
                      onChange={(e) => setCustomerNotes(e.target.value)}
                      className="bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                      placeholder="یادداشت یا توضیحات اضافی خود را وارد کنید"
                      rows={3}
                    />
                  </div>
                </CardContent>
              </Card>

              {/* Payment Information */}
              <Card className="bg-white/10 border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">اطلاعات پرداخت</CardTitle>
                  <CardDescription className="text-gray-300">
                    پس از ثبت سفارش، اطلاعات حساب بانکی برای شما نمایش داده خواهد شد
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="bg-orange-500/20 border border-orange-500/30 rounded-lg p-4">
                    <div className="flex items-center gap-3">
                      <CreditCard className="h-6 w-6 text-orange-400" />
                      <div>
                        <h4 className="text-orange-400 font-semibold">پرداخت نقدی</h4>
                        <p className="text-orange-300 text-sm">
                          پس از ثبت سفارش، اطلاعات حساب بانکی و نحوه پرداخت برای شما ارسال خواهد شد
                        </p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Order Summary */}
            <div className="lg:col-span-1">
              <Card className="bg-white/10 border-white/20 sticky top-6">
                <CardHeader>
                  <CardTitle className="text-white">خلاصه سفارش</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Order Items */}
                  <div className="space-y-3">
                    {cart.items.map((item) => (
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
                          <h4 className="text-white text-sm font-medium">{item.product.name}</h4>
                          <p className="text-gray-400 text-xs">
                            {item.quantity} عدد × {item.product.price.toLocaleString()} تومان
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="text-white font-semibold text-sm">
                            {item.total_price.toLocaleString()} تومان
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>

                  <hr className="border-white/20" />

                  {/* Order Totals */}
                  <div className="space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-gray-300">تعداد محصولات:</span>
                      <span className="text-white font-semibold">{cart.total_items}</span>
                    </div>
                    
                    <div className="flex justify-between items-center">
                      <span className="text-gray-300">قیمت کل:</span>
                      <span className="text-white font-semibold">{cart.total_price.toLocaleString()} تومان</span>
                    </div>
                    
                    <div className="flex justify-between items-center">
                      <span className="text-gray-300">هزینه ارسال:</span>
                      <span className="text-white font-semibold">رایگان</span>
                    </div>
                    
                    <hr className="border-white/20" />
                    
                    <div className="flex justify-between items-center text-lg">
                      <span className="text-white font-bold">مبلغ قابل پرداخت:</span>
                      <span className="text-orange-400 font-bold">{cart.total_price.toLocaleString()} تومان</span>
                    </div>
                  </div>

                  {/* Submit Button */}
                  <Button
                    type="submit"
                    className="w-full bg-orange-600 hover:bg-orange-700 text-white"
                    disabled={submitting}
                  >
                    {submitting ? (
                      <div className="flex items-center gap-2">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                        در حال ثبت سفارش...
                      </div>
                    ) : (
                      <>
                        <CreditCard className="h-4 w-4 mr-2" />
                        ثبت سفارش
                      </>
                    )}
                  </Button>

                  <p className="text-gray-400 text-xs text-center">
                    با کلیک روی دکمه بالا، شما قوانین و شرایط فروشگاه را پذیرفته‌اید
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function CheckoutPage() {
  return (
    <ProtectedRoute>
      <CheckoutContent />
    </ProtectedRoute>
  );
} 