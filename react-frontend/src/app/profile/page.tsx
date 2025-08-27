'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useAuth } from '@/contexts/AuthContext';
import ProtectedRoute from '@/components/ProtectedRoute';
import Link from 'next/link';
import { 
  ArrowLeft, 
  User, 
  Settings, 
  Shield,
  Users,
  FileText,
  Printer,
  Keyboard,
  ShoppingCart,
  BarChart3,
  DollarSign,
  Clock,
  CheckCircle,
  AlertCircle,
  XCircle,
  Eye,
  Edit,
  Trash2
} from 'lucide-react';
import { GlowCard } from '@/components/ui/spotlight-card';

interface AdminStats {
  total_users: number;
  total_print_orders: number;
  total_typing_orders: number;
  total_shop_orders: number;
  pending_orders: number;
  revenue_today: number;
  revenue_month: number;
}

function ProfileContent() {
  const { user } = useAuth();
  const [adminStats, setAdminStats] = useState<AdminStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [profileData, setProfileData] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    email: user?.email || '',
  });

  useEffect(() => {
    if (user?.is_staff) {
      fetchAdminStats();
    } else {
      setLoading(false);
    }
  }, [user]);

  const fetchAdminStats = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/admin-dashboard/api/stats/', {
        credentials: 'include'
      });
      if (response.ok) {
        const data = await response.json();
        setAdminStats(data);
      }
    } catch (error) {
      console.error('Error fetching admin stats:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <div className="flex items-center gap-4 mb-6">
          <Link href="/dashboard">
            <Button variant="outline" className="border-white/20 text-white hover:bg-white/10">
              <ArrowLeft className="h-4 w-4 mr-2" />
              بازگشت به داشبورد
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">
              <User className="h-8 w-8 inline mr-2" />
              پروفایل کاربری
            </h1>
            <p className="text-gray-300">
              مدیریت اطلاعات شخصی و دسترسی سریع به بخش‌های مهم سیستم
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Profile Information */}
        <div className="lg:col-span-1">
          <GlowCard glowColor="blue" size="lg">
            <Card className="bg-white/10 border-white/20 h-full">
              <CardHeader>
                <CardTitle className="text-white text-xl">
                  <User className="h-5 w-5 inline mr-2" />
                  اطلاعات شخصی
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-center mb-6">
                  <div className="w-24 h-24 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full mx-auto mb-4 flex items-center justify-center">
                    <User className="h-12 w-12 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-white">
                    {user?.first_name} {user?.last_name}
                  </h3>
                  <p className="text-gray-300">{user?.email}</p>
                  <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium mt-2 ${
                    user?.is_staff 
                      ? 'bg-red-500/20 text-red-300 border border-red-500/30' 
                      : 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                  }`}>
                    {user?.is_staff ? 'مدیر سیستم' : 'کاربر عادی'}
                  </span>
                </div>

                <div className="space-y-3">
                  <div>
                    <label className="block text-white text-sm mb-1">نام</label>
                    <Input
                      value={profileData.first_name}
                      onChange={(e) => setProfileData(prev => ({ ...prev, first_name: e.target.value }))}
                      className="bg-white/10 border-white/20 text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-white text-sm mb-1">نام خانوادگی</label>
                    <Input
                      value={profileData.last_name}
                      onChange={(e) => setProfileData(prev => ({ ...prev, last_name: e.target.value }))}
                      className="bg-white/10 border-white/20 text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-white text-sm mb-1">ایمیل</label>
                    <Input
                      value={profileData.email}
                      onChange={(e) => setProfileData(prev => ({ ...prev, email: e.target.value }))}
                      className="bg-white/10 border-white/20 text-white"
                      disabled
                    />
                  </div>
                </div>

                <Button className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white">
                  <Edit className="h-4 w-4 mr-2" />
                  بروزرسانی اطلاعات
                </Button>
              </CardContent>
            </Card>
          </GlowCard>
        </div>

        {/* Quick Access & Admin Panel */}
        <div className="lg:col-span-2 space-y-6">
          {/* Admin Stats */}
          {user?.is_staff && (
            <GlowCard glowColor="red" size="lg">
              <Card className="bg-white/10 border-white/20">
                <CardHeader>
                  <CardTitle className="text-white text-xl">
                    <Shield className="h-5 w-5 inline mr-2" />
                    آمار کلی سیستم - دسترسی مدیر
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {loading ? (
                    <div className="text-center text-gray-300 py-8">
                      در حال بارگذاری آمار...
                    </div>
                  ) : (
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="bg-white/5 rounded-lg p-4 text-center">
                        <Users className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                        <p className="text-2xl font-bold text-white">{adminStats?.total_users || 0}</p>
                        <p className="text-gray-400 text-sm">کل کاربران</p>
                      </div>
                      
                      <div className="bg-white/5 rounded-lg p-4 text-center">
                        <FileText className="h-8 w-8 text-green-400 mx-auto mb-2" />
                        <p className="text-2xl font-bold text-white">
                          {(adminStats?.total_print_orders || 0) + (adminStats?.total_typing_orders || 0)}
                        </p>
                        <p className="text-gray-400 text-sm">کل سفارشات</p>
                      </div>
                      
                      <div className="bg-white/5 rounded-lg p-4 text-center">
                        <Clock className="h-8 w-8 text-yellow-400 mx-auto mb-2" />
                        <p className="text-2xl font-bold text-white">{adminStats?.pending_orders || 0}</p>
                        <p className="text-gray-400 text-sm">در انتظار بررسی</p>
                      </div>
                      
                      <div className="bg-white/5 rounded-lg p-4 text-center">
                        <DollarSign className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                        <p className="text-2xl font-bold text-white">
                          {((adminStats?.revenue_month || 0) / 1000000).toFixed(1)}M
                        </p>
                        <p className="text-gray-400 text-sm">درآمد ماه (تومان)</p>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            </GlowCard>
          )}

          {/* Quick Access - Services */}
          <GlowCard glowColor="green" size="lg">
            <Card className="bg-white/10 border-white/20">
              <CardHeader>
                <CardTitle className="text-white text-xl">
                  <Settings className="h-5 w-5 inline mr-2" />
                  دسترسی سریع - خدمات
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <Link href="/print-service">
                    <Button className="w-full h-20 bg-gradient-to-br from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white flex-col">
                      <Printer className="h-6 w-6 mb-2" />
                      خدمات چاپ
                    </Button>
                  </Link>
                  
                  <Link href="/typing-service">
                    <Button className="w-full h-20 bg-gradient-to-br from-purple-500 to-violet-500 hover:from-purple-600 hover:to-violet-600 text-white flex-col">
                      <Keyboard className="h-6 w-6 mb-2" />
                      خدمات تایپ
                    </Button>
                  </Link>
                  
                  <Link href="/shop">
                    <Button className="w-full h-20 bg-gradient-to-br from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 text-white flex-col">
                      <ShoppingCart className="h-6 w-6 mb-2" />
                      فروشگاه دیجیتال
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          </GlowCard>

          {/* Admin Quick Actions */}
          {user?.is_staff && (
            <GlowCard glowColor="orange" size="lg">
              <Card className="bg-white/10 border-white/20">
                <CardHeader>
                  <CardTitle className="text-white text-xl">
                    <Shield className="h-5 w-5 inline mr-2" />
                    عملیات سریع مدیریت
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    <a 
                      href="http://127.0.0.1:8000/admin-dashboard/users/"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block"
                    >
                      <Button variant="outline" className="w-full h-16 border-white/20 text-white hover:bg-white/10 flex-col">
                        <Users className="h-5 w-5 mb-1" />
                        <span className="text-xs">مدیریت کاربران</span>
                      </Button>
                    </a>
                    
                    <a 
                      href="http://127.0.0.1:8000/admin-dashboard/print-orders/"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block"
                    >
                      <Button variant="outline" className="w-full h-16 border-white/20 text-white hover:bg-white/10 flex-col">
                        <Printer className="h-5 w-5 mb-1" />
                        <span className="text-xs">سفارشات چاپ</span>
                      </Button>
                    </a>
                    
                    <a 
                      href="http://127.0.0.1:8000/admin-dashboard/typing-orders/"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block"
                    >
                      <Button variant="outline" className="w-full h-16 border-white/20 text-white hover:bg-white/10 flex-col">
                        <Keyboard className="h-5 w-5 mb-1" />
                        <span className="text-xs">سفارشات تایپ</span>
                      </Button>
                    </a>
                    
                    <a 
                      href="http://127.0.0.1:8000/admin-dashboard/shop-orders/"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block"
                    >
                      <Button variant="outline" className="w-full h-16 border-white/20 text-white hover:bg-white/10 flex-col">
                        <ShoppingCart className="h-5 w-5 mb-1" />
                        <span className="text-xs">سفارشات فروشگاه</span>
                      </Button>
                    </a>
                    
                    <a 
                      href="http://127.0.0.1:8000/admin-dashboard/settings/"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block"
                    >
                      <Button variant="outline" className="w-full h-16 border-white/20 text-white hover:bg-white/10 flex-col">
                        <Settings className="h-5 w-5 mb-1" />
                        <span className="text-xs">تنظیمات</span>
                      </Button>
                    </a>
                    
                    <a 
                      href="http://127.0.0.1:8000/admin-dashboard/reports/"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block"
                    >
                      <Button variant="outline" className="w-full h-16 border-white/20 text-white hover:bg-white/10 flex-col">
                        <BarChart3 className="h-5 w-5 mb-1" />
                        <span className="text-xs">گزارشات</span>
                      </Button>
                    </a>
                    
                    <a 
                      href="http://127.0.0.1:8000/admin-dashboard/pricing/"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block"
                    >
                      <Button variant="outline" className="w-full h-16 border-white/20 text-white hover:bg-white/10 flex-col">
                        <DollarSign className="h-5 w-5 mb-1" />
                        <span className="text-xs">مدیریت قیمت</span>
                      </Button>
                    </a>
                    
                    <a 
                      href="http://127.0.0.1:8000/admin/"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block"
                    >
                      <Button variant="outline" className="w-full h-16 border-red-400/30 text-red-300 hover:bg-red-400/10 flex-col border-2">
                        <Shield className="h-5 w-5 mb-1" />
                        <span className="text-xs">پنل Django</span>
                      </Button>
                    </a>
                  </div>
                </CardContent>
              </Card>
            </GlowCard>
          )}

          {/* Recent Activities - for regular users */}
          {!user?.is_staff && (
            <GlowCard glowColor="purple" size="lg">
              <Card className="bg-white/10 border-white/20">
                <CardHeader>
                  <CardTitle className="text-white text-xl">
                    <Clock className="h-5 w-5 inline mr-2" />
                    فعالیت‌های اخیر
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center gap-3 p-3 bg-white/5 rounded-lg">
                      <CheckCircle className="h-5 w-5 text-green-400" />
                      <div className="flex-1">
                        <p className="text-white text-sm">سفارش چاپ #1234 تکمیل شد</p>
                        <p className="text-gray-400 text-xs">2 ساعت پیش</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3 p-3 bg-white/5 rounded-lg">
                      <AlertCircle className="h-5 w-5 text-yellow-400" />
                      <div className="flex-1">
                        <p className="text-white text-sm">سفارش تایپ #5678 در انتظار پرداخت</p>
                        <p className="text-gray-400 text-xs">1 روز پیش</p>
                      </div>
                    </div>
                  </div>

                  <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-3">
                    <Link href="/print-orders">
                      <Button variant="outline" className="w-full border-white/20 text-white hover:bg-white/10">
                        <Eye className="h-4 w-4 mr-2" />
                        سفارشات چاپ
                      </Button>
                    </Link>
                    <Link href="/typing-orders">
                      <Button variant="outline" className="w-full border-white/20 text-white hover:bg-white/10">
                        <Eye className="h-4 w-4 mr-2" />
                        سفارشات تایپ
                      </Button>
                    </Link>
                    <Link href="/shop-orders">
                      <Button variant="outline" className="w-full border-white/20 text-white hover:bg-white/10">
                        <Eye className="h-4 w-4 mr-2" />
                        سفارشات فروشگاه
                      </Button>
                    </Link>
                  </div>
                </CardContent>
              </Card>
            </GlowCard>
          )}
        </div>
      </div>
    </div>
  );
}

export default function ProfilePage() {
  return (
    <ProtectedRoute>
      <ProfileContent />
    </ProtectedRoute>
  );
}
