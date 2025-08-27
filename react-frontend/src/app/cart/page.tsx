'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { digitalShopAPI } from '@/lib/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import ProtectedRoute from '@/components/ProtectedRoute';
import { 
  ShoppingCart, 
  Trash2,
  Plus,
  Minus,
  ArrowLeft,
  Package,
  CreditCard
} from 'lucide-react';
import Link from 'next/link';

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

function CartContent() {
  const { user } = useAuth();
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(true);
  const [updatingItem, setUpdatingItem] = useState<number | null>(null);
  const [removingItem, setRemovingItem] = useState<number | null>(null);

  useEffect(() => {
    fetchCart();

    const handleStorageChange = (event: StorageEvent) => {
      if (event.key === 'shop_cart_items' || event.key === 'cart' || event.key === 'cartCount') {
        fetchCart();
      }
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  const fetchCart = async () => {
    try {
      setLoading(true);
      
      // Read directly from localStorage (prefer canonical key)
      let parsed: any;
      try {
        parsed = JSON.parse(localStorage.getItem('shop_cart_items') || '[]');
      } catch {
        parsed = [];
      }
      // Fallback to legacy key 'cart'
      if (!Array.isArray(parsed)) {
        try {
          parsed = JSON.parse(localStorage.getItem('cart') || '[]');
        } catch {
          parsed = [];
        }
      }
      // Normalize if legacy object format was used { items: [...] }
      const localCart = Array.isArray(parsed)
        ? parsed
        : (parsed && Array.isArray(parsed.items) ? parsed.items : []);
      console.log('Cart page - localStorage cart:', localCart);
      
      if (localCart.length > 0) {
        const totalPrice = localCart.reduce((sum: number, item: any) => sum + (item.price * item.quantity), 0);
        const cartData = {
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
        };
        
        console.log('Cart page - setting cart data:', cartData);
        setCart(cartData);
      } else {
        console.log('Cart page - localStorage cart is empty');
        setCart({ items: [], total_items: 0, total_price: 0 });
      }
      
    } catch (error) {
      console.error('Error in fetchCart:', error);
      setCart({ items: [], total_items: 0, total_price: 0 });
    } finally {
      setLoading(false);
    }
  };

  const updateCartItem = async (itemId: number, quantity: number) => {
    if (quantity <= 0) {
      await removeCartItem(itemId);
      return;
    }

    try {
      setUpdatingItem(itemId);
      
      // Use localStorage directly (bypassing API)
      console.log('Updating cart item in localStorage...');
      
      const localCart = JSON.parse(localStorage.getItem('shop_cart_items') || localStorage.getItem('cart') || '[]');
      const itemIndex = localCart.findIndex((item: any) => item.id === itemId);
      
      if (itemIndex !== -1) {
        localCart[itemIndex].quantity = quantity;
        localStorage.setItem('shop_cart_items', JSON.stringify(localCart));
        localStorage.setItem('cart', JSON.stringify(localCart));
        
        // Update cart count
        const newCartCount = localCart.reduce((sum: number, item: any) => sum + item.quantity, 0);
        localStorage.setItem('cartCount', newCartCount.toString());
        
        console.log('Updated cart item in localStorage');
        await fetchCart(); // Refresh cart
      }
      
    } catch (error) {
      console.error('Error updating cart item:', error);
      alert('خطا در به‌روزرسانی سبد خرید');
    } finally {
      setUpdatingItem(null);
    }
  };

  const removeCartItem = async (itemId: number) => {
    try {
      setRemovingItem(itemId);
      
      // Use localStorage directly (bypassing API)
      console.log('Removing cart item from localStorage...');
      
      const localCart = JSON.parse(localStorage.getItem('shop_cart_items') || localStorage.getItem('cart') || '[]');
      const filteredCart = localCart.filter((item: any) => item.id !== itemId);
      localStorage.setItem('shop_cart_items', JSON.stringify(filteredCart));
      localStorage.setItem('cart', JSON.stringify(filteredCart));
      
      // Update cart count
      const newCartCount = filteredCart.reduce((sum: number, item: any) => sum + item.quantity, 0);
      localStorage.setItem('cartCount', newCartCount.toString());
      
      console.log('Removed cart item from localStorage');
      await fetchCart(); // Refresh cart
      
    } catch (error) {
      console.error('Error removing cart item:', error);
      alert('خطا در حذف محصول از سبد خرید');
    } finally {
      setRemovingItem(null);
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
          {/* Header */}
          <div className="flex items-center gap-4 mb-8">
            <Link href="/shop">
              <Button variant="outline" className="border-white/20 text-white hover:bg-white/10">
                <ArrowLeft className="h-4 w-4 mr-2" />
                بازگشت به فروشگاه
              </Button>
            </Link>
            <h1 className="text-3xl font-bold text-white">سبد خرید</h1>
            
            {/* Debug button */}
            <Button
              variant="outline"
              size="sm"
              className="border-yellow-400 text-yellow-400 hover:bg-yellow-400/10"
              onClick={() => {
                const localCart = JSON.parse(localStorage.getItem('cart') || '[]');
                const cartCount = localStorage.getItem('cartCount') || '0';
                console.log('Cart page debug - localStorage cart:', localCart);
                console.log('Cart page debug - cartCount:', cartCount);
                console.log('Cart page debug - current cart state:', cart);
                alert(`Cart Page Debug:\nlocalStorage Items: ${localCart.length}\nlocalStorage Cart Count: ${cartCount}\nCurrent State Items: ${cart?.items?.length || 0}\nlocalStorage Contents: ${JSON.stringify(localCart, null, 2)}`);
              }}
            >
              دیباگ سبد خرید
            </Button>
            
            {/* Refresh cart button */}
            <Button
              variant="outline"
              size="sm"
              className="border-blue-400 text-blue-400 hover:bg-blue-400/10"
              onClick={() => {
                console.log('Refreshing cart...');
                fetchCart();
              }}
            >
              تازه‌سازی سبد خرید
            </Button>
            
            {/* Force refresh button */}
            <Button
              variant="outline"
              size="sm"
              className="border-red-400 text-red-400 hover:bg-red-400/10"
              onClick={() => {
                console.log('Force refreshing cart...');
                setCart(null);
                setLoading(true);
                setTimeout(() => {
                  fetchCart();
                }, 100);
              }}
            >
              تازه‌سازی اجباری
            </Button>
            
            {/* Test localStorage button */}
            <Button
              variant="outline"
              size="sm"
              className="border-green-400 text-green-400 hover:bg-green-400/10"
              onClick={() => {
                // Test if localStorage is working
                const testKey = 'test_key';
                const testValue = 'test_value';
                
                try {
                  localStorage.setItem(testKey, testValue);
                  const retrievedValue = localStorage.getItem(testKey);
                  localStorage.removeItem(testKey);
                  
                  if (retrievedValue === testValue) {
                    alert('localStorage کار می‌کند!');
                  } else {
                    alert('localStorage مشکل دارد!');
                  }
                } catch (error) {
                  alert(`localStorage خطا دارد: ${error}`);
                }
              }}
            >
              تست localStorage
            </Button>
            
            {/* Test Add Product button */}
            <Button
              variant="outline"
              size="sm"
              className="border-orange-400 text-orange-400 hover:bg-orange-400/10"
              onClick={() => {
                // Add a test product directly to localStorage
                const testProduct = {
                  id: 999,
                  name: 'محصول تست',
                  price: 1000,
                  image: null,
                  quantity: 1
                };
                
                const existingCart = JSON.parse(localStorage.getItem('cart') || '[]');
                existingCart.push(testProduct);
                localStorage.setItem('cart', JSON.stringify(existingCart));
                
                const newCartCount = existingCart.reduce((sum: number, item: any) => sum + item.quantity, 0);
                localStorage.setItem('cartCount', newCartCount.toString());
                
                alert('محصول تست اضافه شد! حالا سبد خرید را تازه کنید.');
              }}
            >
              افزودن محصول تست
            </Button>
          </div>

          {/* Empty Cart */}
          <Card className="bg-white/10 border-white/20">
            <CardContent className="p-12 text-center">
              <ShoppingCart className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-white mb-2">سبد خرید شما خالی است</h3>
              <p className="text-gray-300 mb-6">محصولات مورد نظر خود را به سبد خرید اضافه کنید</p>
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
          <Link href="/shop">
            <Button variant="outline" className="border-white/20 text-white hover:bg-white/10">
              <ArrowLeft className="h-4 w-4 mr-2" />
              بازگشت به فروشگاه
            </Button>
          </Link>
          <h1 className="text-3xl font-bold text-white">سبد خرید</h1>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Cart Items */}
          <div className="lg:col-span-2">
            <Card className="bg-white/10 border-white/20">
              <CardHeader>
                <CardTitle className="text-white">محصولات سبد خرید ({cart.total_items})</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {cart.items.map((item) => (
                  <div key={item.id} className="flex items-center gap-4 p-4 bg-white/5 rounded-lg">
                    {/* Product Image */}
                    <div className="w-20 h-20 bg-white/10 rounded-lg flex items-center justify-center overflow-hidden">
                      {item.product.image ? (
                        <img
                          src={item.product.image}
                          alt={item.product.name}
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <Package className="h-8 w-8 text-gray-400" />
                      )}
                    </div>

                    {/* Product Info */}
                    <div className="flex-1">
                      <h3 className="text-white font-semibold mb-1">{item.product.name}</h3>
                      <p className="text-gray-300 text-sm">
                        {item.product.price.toLocaleString()} تومان
                      </p>
                    </div>

                    {/* Quantity Controls */}
                    <div className="flex items-center gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        className="border-white/20 text-white hover:bg-white/10"
                        onClick={() => updateCartItem(item.id, item.quantity - 1)}
                        disabled={updatingItem === item.id}
                      >
                        <Minus className="h-4 w-4" />
                      </Button>
                      
                      <Input
                        type="number"
                        value={item.quantity}
                        onChange={(e) => updateCartItem(item.id, parseInt(e.target.value) || 0)}
                        className="w-16 text-center bg-white/10 border-white/20 text-white"
                        min="1"
                        disabled={updatingItem === item.id}
                      />
                      
                      <Button
                        variant="outline"
                        size="sm"
                        className="border-white/20 text-white hover:bg-white/10"
                        onClick={() => updateCartItem(item.id, item.quantity + 1)}
                        disabled={updatingItem === item.id}
                      >
                        <Plus className="h-4 w-4" />
                      </Button>
                    </div>

                    {/* Total Price */}
                    <div className="text-right">
                      <p className="text-white font-bold">
                        {item.total_price.toLocaleString()} تومان
                      </p>
                    </div>

                    {/* Remove Button */}
                    <Button
                      variant="ghost"
                      size="sm"
                      className="text-red-400 hover:text-red-300 hover:bg-red-400/10"
                      onClick={() => removeCartItem(item.id)}
                      disabled={removingItem === item.id}
                    >
                      {removingItem === item.id ? (
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-red-400"></div>
                      ) : (
                        <Trash2 className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                ))}
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

                <div className="space-y-3 pt-4">
                  <Link href="/checkout" className="w-full">
                    <Button className="w-full bg-orange-600 hover:bg-orange-700 text-white">
                      <CreditCard className="h-4 w-4 mr-2" />
                      ادامه خرید
                    </Button>
                  </Link>
                  
                  <Link href="/shop" className="w-full">
                    <Button variant="outline" className="w-full border-white/20 text-white hover:bg-white/10">
                      <Package className="h-4 w-4 mr-2" />
                      افزودن محصول بیشتر
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function CartPage() {
  return (
    <ProtectedRoute>
      <CartContent />
    </ProtectedRoute>
  );
}
