'use client';

import { useEffect, useState, use as usePromise } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { digitalShopAPI } from '@/lib/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import ProtectedRoute from '@/components/ProtectedRoute';
import { 
  ArrowLeft,
  Package,
  Star,
  Heart,
  ShoppingCart,
  Minus,
  Plus
} from 'lucide-react';
import Link from 'next/link';
import { showToast } from '@/lib/utils';

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
  attributes: Array<{
    name: string;
    value: string;
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

function ProductDetailContent({ params }: { params: { id: string } }) {
  const { user } = useAuth();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [addingToCart, setAddingToCart] = useState(false);
  const [selectedImage, setSelectedImage] = useState(0);

  useEffect(() => {
    fetchProduct();
  }, [params.id]);

  const fetchProduct = async () => {
    try {
      setLoading(true);
      const response = await digitalShopAPI.getProduct(params.id);
      
      if (response.success && response.product) {
        setProduct(response.product);
      } else {
        // If API fails, try to get from localStorage or show error
        console.error('Product not found');
        setProduct(null);
      }
    } catch (error) {
      console.error('Error fetching product:', error);
      setProduct(null);
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = async () => {
    if (!product) return;

    try {
      setAddingToCart(true);
      
      console.log('=== PRODUCT DETAIL ADD TO CART DEBUG START ===');
      console.log('Adding product to cart:', product.name, 'Quantity:', quantity);
      
      // Skip API call and use localStorage directly
      const existingCart = JSON.parse(localStorage.getItem('shop_cart_items') || localStorage.getItem('cart') || '[]');
      console.log('Existing cart from localStorage:', existingCart);
      
      const existingItem = existingCart.find((item: any) => item.id === product.id);
      
      if (existingItem) {
        existingItem.quantity += quantity;
        console.log('Updated existing item quantity to:', existingItem.quantity);
      } else {
        const imageUrl = product.images[0]?.image ? digitalShopAPI.getImageUrl(product.images[0].image) : null;
        const newCartItem = {
          id: product.id,
          name: product.name,
          price: product.price,
          image: imageUrl,
          quantity: quantity
        };
        existingCart.push(newCartItem);
        console.log('Added new item to cart:', newCartItem);
      }
      
      // Save to localStorage (with safeguard)
      try {
        localStorage.setItem('shop_cart_items', JSON.stringify(existingCart));
        localStorage.setItem('cart', JSON.stringify(existingCart));
        console.log('Saved cart to localStorage:', existingCart);
      } catch (e) {
        console.error('localStorage setItem failed:', e);
      }
      
      // Verify localStorage was saved correctly
      const savedCart = JSON.parse(localStorage.getItem('shop_cart_items') || localStorage.getItem('cart') || '[]');
      console.log('Verified saved cart from localStorage:', savedCart);
      console.log('Saved cart length:', savedCart.length);
      
      // Calculate new cart count
      const newCartCount = existingCart.reduce((sum: number, item: any) => sum + item.quantity, 0);
      try {
        localStorage.setItem('cartCount', newCartCount.toString());
      } catch (e) {
        console.error('localStorage setItem cartCount failed:', e);
      }
      console.log('Updated cart count to:', newCartCount);
      
      showToast(`محصول "${product.name}" به سبد خرید اضافه شد! تعداد: ${quantity}`, 'success');
      // Redirect to cart to make result visible immediately
      window.location.href = '/cart';
      console.log('=== PRODUCT DETAIL ADD TO CART DEBUG END ===');
      
    } catch (error) {
      console.error('Error adding to cart:', error);
      showToast('خطا در افزودن به سبد خرید', 'error');
    } finally {
      setAddingToCart(false);
    }
  };

  const incrementQuantity = () => {
    if (product && quantity < product.stock_quantity) {
      setQuantity(quantity + 1);
    }
  };

  const decrementQuantity = () => {
    if (quantity > 1) {
      setQuantity(quantity - 1);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="text-white text-xl">در حال بارگذاری...</div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center gap-4 mb-8">
            <Link href="/shop">
              <Button variant="outline" className="border-white/20 text-white hover:bg-white/10">
                <ArrowLeft className="h-4 w-4 mr-2" />
                بازگشت به فروشگاه
              </Button>
            </Link>
          </div>

          <Card className="bg-white/10 border-white/20">
            <CardContent className="p-12 text-center">
              <Package className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-white mb-2">محصول یافت نشد</h3>
              <p className="text-gray-300 mb-6">محصول مورد نظر شما در دسترس نیست</p>
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
          <div>
            <h1 className="text-3xl font-bold text-white">{product.name}</h1>
            <p className="text-gray-300">SKU: {product.sku}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Product Images */}
          <div>
            <Card className="bg-white/10 border-white/20">
              <CardContent className="p-6">
                {/* Main Image */}
                <div className="aspect-square bg-white/5 rounded-lg mb-4 flex items-center justify-center overflow-hidden">
                  {product.images && product.images.length > 0 ? (
                    <img
                      src={digitalShopAPI.getImageUrl(product.images[selectedImage].image) || ''}
                      alt={product.name}
                      className="w-full h-full object-cover rounded-lg"
                    />
                  ) : (
                    <Package className="h-32 w-32 text-gray-400" />
                  )}
                </div>

                {/* Thumbnail Images */}
                {product.images && product.images.length > 1 && (
                  <div className="flex gap-2 overflow-x-auto">
                    {product.images.map((image, index) => (
                      <button
                        key={image.id}
                        onClick={() => setSelectedImage(index)}
                        className={`w-16 h-16 bg-white/5 rounded-lg flex items-center justify-center overflow-hidden border-2 transition-all ${
                          selectedImage === index 
                            ? 'border-orange-500' 
                            : 'border-transparent hover:border-white/20'
                        }`}
                      >
                        <img
                          src={digitalShopAPI.getImageUrl(image.image) || ''}
                          alt={`${product.name} - تصویر ${index + 1}`}
                          className="w-full h-full object-cover rounded"
                        />
                      </button>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Product Info */}
          <div>
            <Card className="bg-white/10 border-white/20 mb-6">
              <CardContent className="p-6">
                {/* Product Title and Brand */}
                <div className="mb-4">
                  <h2 className="text-2xl font-bold text-white mb-2">{product.name}</h2>
                  {product.brand && (
                    <p className="text-gray-300">برند: {product.brand.name}</p>
                  )}
                  <p className="text-gray-400 text-sm">دسته‌بندی: {product.category.name}</p>
                </div>

                {/* Price */}
                <div className="mb-6">
                  <div className="flex items-center gap-3">
                    <span className="text-3xl font-bold text-white">
                      {product.price.toLocaleString()} تومان
                    </span>
                    {product.compare_price && product.compare_price > product.price && (
                      <span className="text-xl text-gray-400 line-through">
                        {product.compare_price.toLocaleString()} تومان
                      </span>
                    )}
                  </div>
                  {product.compare_price && product.compare_price > product.price && (
                    <span className="inline-block bg-red-500 text-white text-sm px-2 py-1 rounded mt-2">
                      {Math.round(((product.compare_price - product.price) / product.compare_price) * 100)}% تخفیف
                    </span>
                  )}
                </div>

                {/* Stock Status */}
                <div className="mb-6">
                  <div className="flex items-center gap-2 mb-2">
                    <div className={`w-3 h-3 rounded-full ${product.in_stock ? 'bg-green-500' : 'bg-red-500'}`}></div>
                    <span className={`text-sm ${product.in_stock ? 'text-green-400' : 'text-red-400'}`}>
                      {product.in_stock ? 'موجود' : 'ناموجود'}
                    </span>
                  </div>
                  {product.in_stock && (
                    <p className="text-gray-300 text-sm">
                      موجودی: {product.stock_quantity} عدد
                    </p>
                  )}
                </div>

                {/* Quantity Selector */}
                <div className="mb-6">
                  <label className="block text-white text-sm font-medium mb-2">تعداد:</label>
                  <div className="flex items-center gap-3">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={decrementQuantity}
                      disabled={quantity <= 1}
                      className="border-white/20 text-white hover:bg-white/10"
                    >
                      <Minus className="h-4 w-4" />
                    </Button>
                    
                    <Input
                      type="number"
                      value={quantity}
                      onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
                      className="w-20 text-center bg-white/10 border-white/20 text-white"
                      min="1"
                      max={product.stock_quantity}
                    />
                    
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={incrementQuantity}
                      disabled={quantity >= product.stock_quantity}
                      className="border-white/20 text-white hover:bg-white/10"
                    >
                      <Plus className="h-4 w-4" />
                    </Button>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="space-y-3">
                  <Button
                    onClick={handleAddToCart}
                    disabled={!product.in_stock || addingToCart}
                    className="w-full bg-orange-600 hover:bg-orange-700 text-white"
                  >
                    {addingToCart ? (
                      <div className="flex items-center gap-2">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                        در حال افزودن...
                      </div>
                    ) : (
                      <>
                        <ShoppingCart className="h-4 w-4 mr-2" />
                        افزودن به سبد خرید
                      </>
                    )}
                  </Button>
                  
                  <Button
                    variant="outline"
                    className="w-full border-white/20 text-white hover:bg-white/10"
                  >
                    <Heart className="h-4 w-4 mr-2" />
                    افزودن به علاقه‌مندی‌ها
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Product Details */}
            <Card className="bg-white/10 border-white/20">
              <CardHeader>
                <CardTitle className="text-white">جزئیات محصول</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {/* Description */}
                  <div>
                    <h4 className="text-white font-semibold mb-2">توضیحات:</h4>
                    <p className="text-gray-300 text-sm leading-relaxed">
                      {product.description}
                    </p>
                  </div>

                  {/* Attributes */}
                  {product.attributes && product.attributes.length > 0 && (
                    <div>
                      <h4 className="text-white font-semibold mb-2">ویژگی‌ها:</h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                        {product.attributes.map((attr, index) => (
                          <div key={index} className="flex justify-between items-center p-2 bg-white/5 rounded">
                            <span className="text-gray-300 text-sm">{attr.name}:</span>
                            <span className="text-white text-sm font-medium">{attr.value}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Statistics */}
                  <div className="grid grid-cols-2 gap-4 pt-4 border-t border-white/20">
                    <div className="text-center">
                      <p className="text-gray-400 text-sm">تعداد بازدید</p>
                      <p className="text-white font-semibold">{product.view_count || 0}</p>
                    </div>
                    <div className="text-center">
                      <p className="text-gray-400 text-sm">تعداد فروش</p>
                      <p className="text-white font-semibold">{product.sold_count || 0}</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function ProductDetailPage({ params }: { params: Promise<{ id: string }> | { id: string } }) {
  // In Next.js newer versions, params may be a Promise in client components
  // Unwrap it safely using React.use()
  // Support both forms for compatibility
  const resolvedParams = (typeof (params as any).then === 'function')
    ? usePromise(params as Promise<{ id: string }>)
    : (params as { id: string });

  return (
    <ProtectedRoute>
      <ProductDetailContent params={resolvedParams} />
    </ProtectedRoute>
  );
}
