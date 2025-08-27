'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { dashboardAPI } from '@/lib/api';
import { GlowCard } from '@/components/ui/spotlight-card';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import ProtectedRoute from '@/components/ProtectedRoute';
import { 
  Printer, 
  Keyboard, 
  ShoppingCart, 
  User, 
  LogOut, 
  FileText, 
  Package,
  TrendingUp,
  Clock,
  Settings,
  Shield,
  Crown
} from 'lucide-react';
import Link from 'next/link';

interface DashboardStats {
  printOrders: number;
  typingOrders: number;
  shopOrders: number;
  totalOrders: number;
}

function DashboardContent() {
  const { user, logout } = useAuth();
  const [stats, setStats] = useState<DashboardStats>({
    printOrders: 0,
    typingOrders: 0,
    shopOrders: 0,
    totalOrders: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [printOrders, typingOrders, shopOrders] = await Promise.all([
          dashboardAPI.getPrintOrders(),
          dashboardAPI.getTypingOrders(),
          dashboardAPI.getDigitalShopOrders(),
        ]);

        setStats({
          printOrders: printOrders.length || 0,
          typingOrders: typingOrders.length || 0,
          shopOrders: shopOrders.length || 0,
          totalOrders: (printOrders.length || 0) + (typingOrders.length || 0) + (shopOrders.length || 0),
        });
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const handleLogout = async () => {
    await logout();
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
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">
              خوش آمدید، {user?.first_name}!
            </h1>
            <p className="text-gray-300">
              داشبورد مدیریت سفارشات و خدمات
            </p>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-white font-medium">{user?.email}</p>
              <p className="text-gray-400 text-sm">
                {user?.is_staff ? 'مدیر سیستم' : 'کاربر عادی'}
              </p>
            </div>
            <Button
              onClick={handleLogout}
              variant="outline"
              className="border-white/20 text-white hover:bg-white/10"
            >
              <LogOut className="h-4 w-4 mr-2" />
              خروج
            </Button>
          </div>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="max-w-7xl mx-auto mb-8">
        <Card className="bg-white/10 border-white/20">
          <CardHeader>
            <CardTitle className="text-white">آمار کلی</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-white/5 rounded-lg">
                <TrendingUp className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                <p className="text-2xl font-bold text-white">{stats.totalOrders}</p>
                <p className="text-gray-400 text-sm">کل سفارشات</p>
              </div>
              <div className="text-center p-4 bg-white/5 rounded-lg">
                <Printer className="h-8 w-8 text-green-400 mx-auto mb-2" />
                <p className="text-2xl font-bold text-white">{stats.printOrders}</p>
                <p className="text-gray-400 text-sm">سفارشات چاپ</p>
              </div>
              <div className="text-center p-4 bg-white/5 rounded-lg">
                <Keyboard className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                <p className="text-2xl font-bold text-white">{stats.typingOrders}</p>
                <p className="text-gray-400 text-sm">سفارشات تایپ</p>
              </div>
              <div className="text-center p-4 bg-white/5 rounded-lg">
                <ShoppingCart className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                <p className="text-2xl font-bold text-white">{stats.shopOrders}</p>
                <p className="text-gray-400 text-sm">سفارشات فروشگاه</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Service Cards */}
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {/* Print Service */}
          <GlowCard glowColor="green" size="lg">
            <div className="flex flex-col h-full">
              <div className="flex items-center gap-3 mb-4">
                <Printer className="h-8 w-8 text-green-400" />
                <h3 className="text-xl font-bold text-white">خدمات چاپ</h3>
              </div>
              <p className="text-gray-300 mb-6 flex-grow">
                سفارش چاپ اسناد، تصاویر و فایل‌های مختلف با کیفیت بالا
              </p>
              <div className="space-y-3">
                <Link href="/print-service">
                  <Button className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-medium">
                    سفارش جدید
                  </Button>
                </Link>
                <Link href="/print-orders">
                  <Button variant="outline" className="w-full border-white/20 text-white hover:bg-white/10">
                    <FileText className="h-4 w-4 mr-2" />
                    مشاهده سفارشات ({stats.printOrders})
                  </Button>
                </Link>
              </div>
            </div>
          </GlowCard>

          {/* Typing Service */}
          <GlowCard glowColor="purple" size="lg">
            <div className="flex flex-col h-full">
              <div className="flex items-center gap-3 mb-4">
                <Keyboard className="h-8 w-8 text-purple-400" />
                <h3 className="text-xl font-bold text-white">خدمات تایپ</h3>
              </div>
              <p className="text-gray-300 mb-6 flex-grow">
                تایپ و ویرایش متون، اسناد و فایل‌های مختلف با دقت بالا
              </p>
              <div className="space-y-3">
                <Link href="/typing-service">
                  <Button className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-medium">
                    سفارش جدید
                  </Button>
                </Link>
                <Link href="/typing-orders">
                  <Button variant="outline" className="w-full border-white/20 text-white hover:bg-white/10">
                    <FileText className="h-4 w-4 mr-2" />
                    مشاهده سفارشات ({stats.typingOrders})
                  </Button>
                </Link>
              </div>
            </div>
          </GlowCard>

          {/* Digital Shop */}
          <GlowCard glowColor="orange" size="lg">
            <div className="flex flex-col h-full">
              <div className="flex items-center gap-3 mb-4">
                <ShoppingCart className="h-8 w-8 text-orange-400" />
                <h3 className="text-xl font-bold text-white">فروشگاه دیجیتال</h3>
              </div>
              <p className="text-gray-300 mb-6 flex-grow">
                خرید لوازم التحریر، تجهیزات کامپیوتر و محصولات دیجیتال
              </p>
              <div className="space-y-3">
                <Link href="/shop">
                  <Button className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-medium">
                    مشاهده محصولات
                  </Button>
                </Link>
                <Link href="/shop-orders">
                  <Button variant="outline" className="w-full border-white/20 text-white hover:bg-white/10">
                    <Package className="h-4 w-4 mr-2" />
                    مشاهده سفارشات ({stats.shopOrders})
                  </Button>
                </Link>
              </div>
            </div>
          </GlowCard>

          {/* Admin Panel or Quick Actions based on user role */}
          {(user?.is_staff || user?.is_superuser) ? (
            <GlowCard glowColor="red" size="lg">
              <div className="flex flex-col h-full">
                <div className="flex items-center gap-3 mb-4">
                  <Shield className="h-8 w-8 text-red-400" />
                  <h3 className="text-xl font-bold text-white">پنل مدیریت</h3>
                  {user?.is_superuser && <Crown className="h-5 w-5 text-yellow-400" />}
                </div>
                <p className="text-gray-300 mb-6 flex-grow">
                  دسترسی به پنل مدیریت سیستم برای تأیید پرداخت‌ها و تنظیمات
                </p>
                <div className="space-y-3">
                  <Link href="/admin">
                    <Button className="w-full bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white font-medium">
                      <Settings className="h-4 w-4 ml-2" />
                      ورود به پنل مدیریت
                    </Button>
                  </Link>
                  <Link href="/admin/payments/approve">
                    <Button variant="outline" className="w-full border-white/20 text-white hover:bg-white/10">
                      <Shield className="h-4 w-4 mr-2" />
                      تأیید فیش‌های پرداخت
                    </Button>
                  </Link>
                </div>
              </div>
            </GlowCard>
          ) : (
            <GlowCard glowColor="blue" size="lg">
              <div className="flex flex-col h-full">
                <div className="flex items-center gap-3 mb-4">
                  <Clock className="h-8 w-8 text-blue-400" />
                  <h3 className="text-xl font-bold text-white">عملیات سریع</h3>
                </div>
                <p className="text-gray-300 mb-6 flex-grow">
                  دسترسی سریع به مهم‌ترین بخش‌های سیستم
                </p>
                <div className="space-y-3">
                  <Link href="/track-order">
                    <Button variant="outline" className="w-full border-white/20 text-white hover:bg-white/10">
                      پیگیری سفارش
                    </Button>
                  </Link>
                  <Link href="/profile">
                    <Button variant="outline" className="w-full border-white/20 text-white hover:bg-white/10">
                      <User className="h-4 w-4 mr-2" />
                      پروفایل کاربری
                    </Button>
                  </Link>
                </div>
              </div>
            </GlowCard>
          )}
        </div>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <DashboardContent />
    </ProtectedRoute>
  );
} 