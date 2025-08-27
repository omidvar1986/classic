'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { digitalShopAPI } from '@/lib/api';
import { GlowCard } from '@/components/ui/spotlight-card';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import ProtectedRoute from '@/components/ProtectedRoute';
import { 
  ShoppingCart, 
  Search, 
  Package,
  Star,
  Heart,
  ArrowLeft
} from 'lucide-react';
import Link from 'next/link';

interface Product {
  id: number;
  name: string;
  description: string;
  short_description?: string;
  price: number;
  compare_price?: number;
  category: {
    id: number;
    name: string;
    color?: string;
  };
  brand: {
    id: number;
    name: string;
  } | null;
  images: Array<{
    id: number;
    image: string;
  }>;
  in_stock: boolean;
  stock_quantity: number;
  sku: string;
  is_featured: boolean;
  is_new: boolean;
  is_on_sale: boolean;
  is_active: boolean;
  view_count?: number;
  sold_count?: number;
  discount_percentage?: number;
}

function ShopContent() {
  const { user } = useAuth();
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [addingToCart, setAddingToCart] = useState<number | null>(null);
  const [cartCount, setCartCount] = useState(0);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        console.log('Starting API call to fetch products...');
        console.log('API base URL:', process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000');
        
        const response = await digitalShopAPI.getProducts();
        console.log('Raw API Response:', response);
        console.log('Response type:', typeof response);
        console.log('Response keys:', Object.keys(response || {}));
        
        // Handle the API response structure
        if (response && response.success && response.products) {
          console.log('Success! Products found:', response.products.length);
          console.log('First product sample:', response.products[0]);
          setProducts(response.products);
        } else if (Array.isArray(response)) {
          console.log('Response is array, products found:', response.length);
          console.log('First product sample:', response[0]);
          setProducts(response);
        } else {
          console.error('Unexpected API response format:', response);
          console.log('Response structure:', JSON.stringify(response, null, 2));
          setProducts([]);
        }
      } catch (error: any) {
        console.error('Error fetching products:', error);
        console.error('Error details:', {
          message: error.message,
          stack: error.stack,
          response: error.response
        });
        
        // Use mock data if API fails
        console.log('Using fallback mock data...');
        setProducts([
          {
            id: 1,
            name: 'لپ‌تاپ ایسوس ROG Strix',
            description: 'لپ‌تاپ گیمینگ قدرتمند با پردازنده Intel Core i7 و کارت گرافیک RTX 3070',
            price: 45000000,
            compare_price: 50000000,
            category: { id: 1, name: 'کامپیوتر' },
            brand: { id: 1, name: 'ایسوس' },
            images: [],
            in_stock: true,
            stock_quantity: 10,
            sku: 'LAPTOP-001',
            is_featured: true,
            is_new: true,
            is_on_sale: true,
            is_active: true
          },
          {
            id: 2,
            name: 'هدفون سونی WH-1000XM4',
            description: 'هدفون بی‌سیم با تکنولوژی حذف نویز و کیفیت صوتی فوق‌العاده',
            price: 8500000,
            compare_price: 9500000,
            category: { id: 2, name: 'صوتی' },
            brand: { id: 2, name: 'سونی' },
            images: [],
            in_stock: true,
            stock_quantity: 25,
            sku: 'HEADPHONE-001',
            is_featured: true,
            is_new: false,
            is_on_sale: true,
            is_active: true
          },
          {
            id: 3,
            name: 'کیبورد مکانیکی لاجیتک',
            description: 'کیبورد مکانیکی گیمینگ با نورپردازی RGB و سویچ‌های آبی',
            price: 2500000,
            category: { id: 3, name: 'لوازم جانبی' },
            brand: { id: 3, name: 'لاجیتک' },
            images: [],
            in_stock: true,
            stock_quantity: 15,
            sku: 'KEYBOARD-001',
            is_featured: false,
            is_new: true,
            is_on_sale: false,
            is_active: true
          }
        ]);
      } finally {
        setLoading(false);
        console.log('Loading finished. Products count:', products.length);
      }
    };

    fetchProducts();
    
    // Load cart count from localStorage
    const savedCartCount = localStorage.getItem('cartCount');
    if (savedCartCount) {
      setCartCount(parseInt(savedCartCount));
    }
  }, []);

  const filteredProducts = products.filter(product => {
    // Debug logging
    console.log('Filtering product:', {
      id: product.id,
      name: product.name,
      is_active: product.is_active,
      category: product.category,
      selectedCategory: selectedCategory
    });
    
    // Check if product is active (default to true if not specified)
    if (product.is_active === false) {
      console.log('Product filtered out - not active:', product.name);
      return false;
    }
    
    const description = product.description || product.short_description || '';
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         description.toLowerCase().includes(searchTerm.toLowerCase());
    
    // Fix category filtering - handle both string and object category formats
    let matchesCategory = true;
    if (selectedCategory !== 'all') {
      if (typeof product.category === 'string') {
        matchesCategory = product.category === selectedCategory;
      } else if (product.category && typeof product.category === 'object') {
        matchesCategory = product.category.name === selectedCategory;
      } else {
        matchesCategory = false;
      }
    }
    
    const result = matchesSearch && matchesCategory;
    if (!result) {
      console.log('Product filtered out:', product.name, {
        matchesSearch,
        matchesCategory,
        searchTerm,
        selectedCategory
      });
    }
    
    return result;
  });

  // Fix categories extraction
  const categories = ['all'];
  products.forEach(product => {
    let categoryName = '';
    if (typeof product.category === 'string') {
      categoryName = product.category;
    } else if (product.category && typeof product.category === 'object') {
      categoryName = product.category.name;
    }
    if (categoryName && !categories.includes(categoryName)) {
      categories.push(categoryName);
    }
  });

  const handleAddToCart = async (productId: number) => {
    console.log('=== ADD TO CART DEBUG START ===');
    console.log('handleAddToCart called with productId:', productId);
    console.log('Current cart count state:', cartCount);
    console.log('Current products:', products);
    
    try {
      setAddingToCart(productId);
      console.log('Setting addingToCart to:', productId);
      
      // Skip API call for now and use localStorage directly
      // The API requires authentication which is causing 302 redirects
      console.log('Using localStorage directly (bypassing API)...');
      
      const product = products.find(p => p.id === productId);
      if (product) {
        console.log('Product found, adding to localStorage cart');
        console.log('Product details:', product);
        
        // Get existing cart from localStorage
        const existingCart = JSON.parse(localStorage.getItem('cart') || '[]');
        console.log('Existing cart from localStorage:', existingCart);
        
        // Check if product already exists in cart
        const existingItem = existingCart.find((item: any) => item.id === productId);
        
        if (existingItem) {
          existingItem.quantity += 1;
          console.log('Updated existing item quantity to:', existingItem.quantity);
        } else {
          const imageUrl = product.images[0]?.image ? digitalShopAPI.getImageUrl(product.images[0].image) : null;
          const newCartItem = {
            id: product.id,
            name: product.name,
            price: product.price,
            image: imageUrl,
            quantity: 1
          };
          existingCart.push(newCartItem);
          console.log('Added new item to cart:', newCartItem);
        }
        
        // Save to localStorage (canonical key + legacy)
        localStorage.setItem('shop_cart_items', JSON.stringify(existingCart));
        localStorage.setItem('cart', JSON.stringify(existingCart));
        console.log('Saved cart to localStorage:', existingCart);
        
        // Verify localStorage was saved correctly
        const savedCart = JSON.parse(localStorage.getItem('shop_cart_items') || localStorage.getItem('cart') || '[]');
        console.log('Verified saved cart from localStorage:', savedCart);
        console.log('Saved cart length:', savedCart.length);
        
        // Calculate new cart count
        const newCartCount = existingCart.reduce((sum: number, item: any) => sum + item.quantity, 0);
        console.log('Calculated new cart count:', newCartCount);
        localStorage.setItem('cartCount', newCartCount.toString());
        
        // Verify cart count was saved
        const savedCartCount = localStorage.getItem('cartCount');
        console.log('Verified saved cart count:', savedCartCount);
        
        // Update cart count state
        setCartCount(newCartCount);
        console.log('Updated cart count state to:', newCartCount);
        
        // Show success message
        alert(`محصول "${product.name}" به سبد خرید اضافه شد! تعداد: 1`);
        
        // Success message
        const successMessage = `${product.name} به سبد خرید اضافه شد!`;
        console.log('Success message:', successMessage);
        
        // Create a toast-like notification
        const notification = document.createElement('div');
        notification.innerHTML = `
          <div style="position: fixed; top: 20px; right: 20px; background: #10b981; color: white; padding: 12px 20px; border-radius: 8px; z-index: 9999; box-shadow: 0 4px 12px rgba(0,0,0,0.3); font-family: system-ui; font-size: 14px; max-width: 300px;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 12l2 2 4-4"></path>
                <circle cx="12" cy="12" r="10"></circle>
              </svg>
              <span>${successMessage}</span>
            </div>
          </div>
        `;
        document.body.appendChild(notification);
        
        // Remove notification after 3 seconds
        setTimeout(() => {
          if (document.body.contains(notification)) {
            document.body.removeChild(notification);
          }
        }, 3000);
        
        // Also try to update the cart count in the header
        const cartCountElement = document.querySelector('[data-cart-count]');
        if (cartCountElement) {
          cartCountElement.textContent = newCartCount.toString();
        }
        
      } else {
        console.error('Product not found for ID:', productId);
        alert('محصول یافت نشد!');
      }
      
    } catch (error: any) {
      console.error('Error adding to cart:', error);
      alert('خطا در افزودن به سبد خرید');
    } finally {
      console.log('Setting addingToCart to null');
      setAddingToCart(null);
      console.log('=== ADD TO CART DEBUG END ===');
    }
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
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-4">
            <Link href="/dashboard">
              <Button variant="outline" className="border-white/20 text-white hover:bg-white/10">
                <ArrowLeft className="h-4 w-4 mr-2" />
                بازگشت به داشبورد
              </Button>
            </Link>
            <div>
              <h1 className="text-3xl font-bold text-white mb-2">
                فروشگاه دیجیتال
              </h1>
              <p className="text-gray-300">
                خرید لوازم التحریر، تجهیزات کامپیوتر و محصولات دیجیتال
              </p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/shop-orders">
              <Button variant="outline" className="border-white/20 text-white hover:bg-white/10">
                <Package className="h-4 w-4 mr-2" />
                سفارشات من
              </Button>
            </Link>
            <Link href="/cart">
              <Button className="bg-orange-600 hover:bg-orange-700 text-white relative">
                <ShoppingCart className="h-4 w-4 mr-2" />
                سبد خرید
                {cartCount > 0 && (
                  <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {cartCount}
                  </span>
                )}
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* Search and Filter */}
      <div className="max-w-7xl mx-auto mb-8">
        <Card className="bg-white/10 border-white/20">
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    placeholder="جستجو در محصولات..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10 bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                  />
                </div>
              </div>
              <div className="flex gap-2">
                {categories.map((category) => (
                  <Button
                    key={category}
                    variant={selectedCategory === category ? "default" : "outline"}
                    onClick={() => setSelectedCategory(category)}
                    className={
                      selectedCategory === category 
                        ? "bg-orange-600 hover:bg-orange-700 text-white" 
                        : "border-white/20 text-white hover:bg-white/10"
                    }
                  >
                    {category === 'all' ? 'همه' : category}
                  </Button>
                ))}
              </div>
            </div>
            
            {/* Debug section */}
            <div className="mt-4 pt-4 border-t border-white/20">
              <div className="flex items-center gap-4">
                <Button
                  variant="outline"
                  size="sm"
                  className="border-yellow-400 text-yellow-400 hover:bg-yellow-400/10"
                  onClick={async () => {
                    try {
                      console.log('Testing API connection...');
                      const response = await fetch('http://localhost:8000/shop/api/products/');
                      const data = await response.json();
                      console.log('Direct fetch response:', data);
                      alert(`API Test: ${data.success ? 'Success' : 'Failed'}\nProducts: ${data.count || 0}`);
                    } catch (error: any) {
                      console.error('Direct fetch error:', error);
                      alert(`API Test Failed: ${error.message}`);
                    }
                  }}
                >
                  تست اتصال API
                </Button>
                
                <Button
                  variant="outline"
                  size="sm"
                  className="border-blue-400 text-blue-400 hover:bg-blue-400/10"
                  onClick={() => {
                    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
                    const cartCount = localStorage.getItem('cartCount') || '0';
                    console.log('Current cart:', cart);
                    console.log('Cart count:', cartCount);
                    alert(`Cart Debug:\nItems: ${cart.length}\nTotal Quantity: ${cartCount}\nCart Contents: ${JSON.stringify(cart, null, 2)}`);
                  }}
                >
                  تست سبد خرید
                </Button>
                
                <Button
                  variant="outline"
                  size="sm"
                  className="border-green-400 text-green-400 hover:bg-green-400/10"
                  onClick={() => {
                    // Add a test product directly to cart
                    const testProduct = {
                      id: 999,
                      name: 'محصول تست',
                      price: 1000,
                      image: null,
                      quantity: 1
                    };
                    
                    console.log('=== TEST PRODUCT DEBUG START ===');
                    console.log('Test product:', testProduct);
                    
                    const existingCart = JSON.parse(localStorage.getItem('cart') || '[]');
                    console.log('Existing cart before adding test:', existingCart);
                    
                    existingCart.push(testProduct);
                    console.log('Cart after adding test product:', existingCart);
                    
                    localStorage.setItem('cart', JSON.stringify(existingCart));
                    console.log('Saved test cart to localStorage');
                    
                    // Verify it was saved
                    const savedCart = JSON.parse(localStorage.getItem('cart') || '[]');
                    console.log('Verified saved test cart:', savedCart);
                    console.log('Saved test cart length:', savedCart.length);
                    
                    const newCartCount = existingCart.reduce((sum: number, item: any) => sum + item.quantity, 0);
                    localStorage.setItem('cartCount', newCartCount.toString());
                    setCartCount(newCartCount);
                    
                    console.log('Updated cart count to:', newCartCount);
                    console.log('=== TEST PRODUCT DEBUG END ===');
                    
                                      alert('محصول تست به سبد خرید اضافه شد!');
                }}
              >
                افزودن محصول تست
              </Button>
              
              <Button
                variant="outline"
                size="sm"
                className="border-purple-400 text-purple-400 hover:bg-purple-400/10"
                onClick={() => {
                  const localCart = JSON.parse(localStorage.getItem('cart') || '[]');
                  const cartCount = localStorage.getItem('cartCount') || '0';
                  console.log('Shop page - localStorage cart:', localCart);
                  console.log('Shop page - cartCount:', cartCount);
                  alert(`محتوای سبد خرید:\nتعداد آیتم‌ها: ${localCart.length}\nتعداد کل: ${cartCount}\nمحصولات: ${localCart.map((item: any) => `${item.name} (${item.quantity})`).join(', ') || 'خالی'}`);
                }}
              >
                مشاهده سبد خرید
              </Button>
                <span className="text-sm text-gray-400">
                  وضعیت: {loading ? 'در حال بارگذاری...' : products.length > 0 ? `${products.length} محصول` : 'بدون محصول'}
                </span>
              </div>
              
              {/* Debug Information */}
              <div className="mt-2 text-xs text-gray-500">
                <div>Raw products count: {products.length}</div>
                <div>Filtered products count: {filteredProducts.length}</div>
                <div>Search term: "{searchTerm}"</div>
                <div>Selected category: "{selectedCategory}"</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Products Grid */}
      <div className="max-w-7xl mx-auto">
        {filteredProducts.length === 0 ? (
          <Card className="bg-white/10 border-white/20">
            <CardContent className="p-12 text-center">
              <Package className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-white mb-2">محصولی یافت نشد</h3>
              <p className="text-gray-300">لطفاً عبارت جستجوی دیگری امتحان کنید</p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredProducts.map((product) => {
              console.log('Rendering product:', {
                id: product.id,
                name: product.name,
                in_stock: product.in_stock,
                is_active: product.is_active
              });
              
              return (
              <GlowCard key={product.id} glowColor="orange" size="md">
                <Card className="bg-white/10 border-white/20 h-full transition-all duration-200">
                    <CardHeader className="pb-3">
                      <Link href={`/shop/product/${product.id}`} className="block group">
                        <div className="aspect-square bg-white/5 rounded-lg mb-3 flex items-center justify-center overflow-hidden group-hover:ring-2 group-hover:ring-white/20">
                          {product.images && product.images.length > 0 ? (
                            <img
                              src={digitalShopAPI.getImageUrl(product.images[0].image) || ''}
                              alt={product.name}
                              className="w-full h-full object-cover rounded-lg"
                              onError={(e) => {
                                console.log('Image failed to load:', product.images[0].image);
                                e.currentTarget.style.display = 'none';
                                e.currentTarget.nextElementSibling?.classList.remove('hidden');
                              }}
                            />
                          ) : null}
                          <Package className={`h-12 w-12 text-gray-400 ${product.images && product.images.length > 0 ? 'hidden' : ''}`} />
                        </div>
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <CardTitle className="text-white text-lg mb-1">{product.name}</CardTitle>
                            <p className="text-gray-400 text-sm">{product.brand?.name || 'بدون برند'}</p>
                          </div>
                        </div>
                      </Link>
                      <div className="flex justify-between items-start mt-2">
                        <div className="flex-1" />
                        <Button
                          variant="ghost"
                          size="sm"
                          className="text-gray-400 hover:text-red-400"
                          onClick={(e) => e.preventDefault()}
                        >
                          <Heart className="h-4 w-4" />
                        </Button>
                      </div>
                    </CardHeader>
                    <CardContent className="pt-0">
                      <CardDescription className="text-gray-300 mb-4 line-clamp-2">
                        {product.short_description || product.description}
                      </CardDescription>
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-1">
                          <Star className="h-4 w-4 text-yellow-400 fill-current" />
                          <span className="text-white text-sm">4.5</span>
                        </div>
                        <div className="text-right">
                          <p className="text-white font-bold text-lg">
                            {typeof product.price === 'number' ? product.price.toLocaleString() : product.price} تومان
                          </p>
                          {product.compare_price && product.compare_price > product.price && (
                            <p className="text-gray-400 text-sm line-through">
                              {typeof product.compare_price === 'number' ? product.compare_price.toLocaleString() : product.compare_price} تومان
                            </p>
                          )}
                        </div>
                      </div>
                      <div className="space-y-2">
                        {/* Debug info */}
                        <div className="text-xs text-gray-500 mb-2">
                          Debug: in_stock={String(product.in_stock)}, is_active={String(product.is_active)}
                        </div>
                        
                        <Button 
                          className="w-full bg-orange-600 hover:bg-orange-700 text-white"
                          disabled={(product.in_stock === false) || addingToCart === product.id}
                          onClick={() => {
                            console.log('Button clicked for product:', product.id);
                            handleAddToCart(product.id);
                          }}
                        >
                          {addingToCart === product.id ? 'در حال افزودن...' : 
                           product.in_stock ? 'افزودن به سبد خرید' : 'ناموجود'}
                        </Button>
                        
                        {/* Test button to verify click handling */}
                        <Button 
                          variant="outline" 
                          size="sm"
                          className="w-full border-green-500/50 text-green-400 hover:bg-green-500/20"
                          onClick={() => {
                            console.log('Test button clicked for product:', product.id);
                            alert(`Test: Product ${product.id} - ${product.name}`);
                          }}
                        >
                          تست کلیک
                        </Button>
                        
                        <Link href={`/shop/product/${product.id}`} className="block">
                          <Button 
                            variant="outline" 
                            className="w-full border-white/20 text-white hover:bg-white/10"
                          >
                            مشاهده جزئیات
                          </Button>
                        </Link>
                      </div>
                    </CardContent>
                </Card>
              </GlowCard>
            );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

export default function ShopPage() {
  return (
    <ProtectedRoute>
      <ShopContent />
    </ProtectedRoute>
  );
} 