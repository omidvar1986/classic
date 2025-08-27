'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import Link from 'next/link';
import {
  CreditCard,
  Users,
  FileText,
  Package,
  ShoppingCart,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  Clock,
  DollarSign,
  Eye,
  Edit,
  Trash2,
  Download
} from 'lucide-react';

interface AdminStats {
  totalUsers: number;
  pendingPayments: number;
  totalOrders: number;
  monthlyRevenue: number;
  printOrders: number;
  typingOrders: number;
  shopOrders: number;
  governmentRequests: number;
}

interface PendingPayment {
  id: number;
  type: 'print' | 'typing' | 'shop';
  customerName: string;
  amount: number;
  submittedAt: string;
  orderNumber?: string;
}

export default function AdminOverview() {
  const [stats, setStats] = useState<AdminStats>({
    totalUsers: 0,
    pendingPayments: 0,
    totalOrders: 0,
    monthlyRevenue: 0,
    printOrders: 0,
    typingOrders: 0,
    shopOrders: 0,
    governmentRequests: 0,
  });
  const [pendingPayments, setPendingPayments] = useState<PendingPayment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Mock data - replace with actual API calls
    setTimeout(() => {
      setStats({
        totalUsers: 1247,
        pendingPayments: 8,
        totalOrders: 156,
        monthlyRevenue: 12500000,
        printOrders: 89,
        typingOrders: 34,
        shopOrders: 33,
        governmentRequests: 12,
      });

      setPendingPayments([
        {
          id: 1,
          type: 'print',
          customerName: 'احمد محمدی',
          amount: 45000,
          submittedAt: '1403/08/15 - 14:30',
          orderNumber: 'PRT-001'
        },
        {
          id: 2,
          type: 'typing',
          customerName: 'فاطمه احمدی',
          amount: 120000,
          submittedAt: '1403/08/15 - 12:15',
          orderNumber: 'TYP-045'
        },
        {
          id: 3,
          type: 'shop',
          customerName: 'علی رضایی',
          amount: 350000,
          submittedAt: '1403/08/15 - 10:45',
          orderNumber: 'SHP-234'
        },
      ]);

      setLoading(false);
    }, 1000);
  }, []);

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('fa-IR').format(amount) + ' تومان';
  };

  const getPaymentTypeIcon = (type: string) => {
    switch (type) {
      case 'print':
        return <FileText className="h-4 w-4" />;
      case 'typing':
        return <Edit className="h-4 w-4" />;
      case 'shop':
        return <ShoppingCart className="h-4 w-4" />;
      default:
        return <FileText className="h-4 w-4" />;
    }
  };

  const getPaymentTypeLabel = (type: string) => {
    switch (type) {
      case 'print':
        return 'چاپ';
      case 'typing':
        return 'تایپ';
      case 'shop':
        return 'فروشگاه';
      default:
        return 'نامشخص';
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-700 rounded w-64 mb-4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-32 bg-gray-700 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-white mb-2">داشبورد مدیریت</h2>
        <p className="text-gray-400">نمای کلی سیستم و عملکرد</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="bg-gradient-to-br from-blue-600 to-blue-700 border-none text-white">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">کل کاربران</CardTitle>
            <Users className="h-4 w-4" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalUsers.toLocaleString('fa-IR')}</div>
            <p className="text-xs text-blue-200">+12% نسبت به ماه قبل</p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-orange-500 to-orange-600 border-none text-white">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">فیش‌های منتظر</CardTitle>
            <AlertCircle className="h-4 w-4" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.pendingPayments}</div>
            <p className="text-xs text-orange-200">نیاز به بررسی فوری</p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-green-500 to-green-600 border-none text-white">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">کل سفارشات</CardTitle>
            <Package className="h-4 w-4" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalOrders.toLocaleString('fa-IR')}</div>
            <p className="text-xs text-green-200">+8% نسبت به هفته قبل</p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-purple-500 to-purple-600 border-none text-white">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">درآمد ماهانه</CardTitle>
            <DollarSign className="h-4 w-4" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatCurrency(stats.monthlyRevenue)}</div>
            <p className="text-xs text-purple-200">+15% نسبت به ماه قبل</p>
          </CardContent>
        </Card>
      </div>

      {/* Service Statistics */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="bg-gray-800 border-gray-700 text-white">
          <CardHeader>
            <CardTitle className="text-lg">آمار خدمات</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <FileText className="h-4 w-4 text-blue-400" />
                  <span className="text-sm">سفارشات چاپ</span>
                </div>
                <span className="font-medium">{stats.printOrders}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Edit className="h-4 w-4 text-purple-400" />
                  <span className="text-sm">سفارشات تایپ</span>
                </div>
                <span className="font-medium">{stats.typingOrders}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <ShoppingCart className="h-4 w-4 text-green-400" />
                  <span className="text-sm">سفارشات فروشگاه</span>
                </div>
                <span className="font-medium">{stats.shopOrders}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <FileText className="h-4 w-4 text-orange-400" />
                  <span className="text-sm">درخواست‌های دولتی</span>
                </div>
                <span className="font-medium">{stats.governmentRequests}</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card className="bg-gray-800 border-gray-700 text-white">
          <CardHeader>
            <CardTitle className="text-lg">عملیات سریع</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <Link href="/admin/payments/approve">
                <Button variant="outline" className="w-full justify-start border-orange-500/50 text-orange-400 hover:bg-orange-500/20">
                  <CreditCard className="h-4 w-4 ml-2" />
                  بررسی فیش‌های پرداخت ({stats.pendingPayments})
                </Button>
              </Link>
              <Link href="/admin/users/list">
                <Button variant="outline" className="w-full justify-start border-blue-500/50 text-blue-400 hover:bg-blue-500/20">
                  <Users className="h-4 w-4 ml-2" />
                  مدیریت کاربران
                </Button>
              </Link>
              <Link href="/admin/pricing/print">
                <Button variant="outline" className="w-full justify-start border-green-500/50 text-green-400 hover:bg-green-500/20">
                  <DollarSign className="h-4 w-4 ml-2" />
                  تنظیم قیمت‌ها
                </Button>
              </Link>
              <Link href="/admin/accessories/manage">
                <Button variant="outline" className="w-full justify-start border-purple-500/50 text-purple-400 hover:bg-purple-500/20">
                  <Package className="h-4 w-4 ml-2" />
                  مدیریت لوازم جانبی
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>

        {/* Pending Payments */}
        <Card className="bg-gray-800 border-gray-700 text-white">
          <CardHeader>
            <CardTitle className="text-lg">فیش‌های منتظر تأیید</CardTitle>
            <CardDescription>آخرین فیش‌های ارسال شده</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {pendingPayments.slice(0, 3).map((payment) => (
                <div key={payment.id} className="flex items-center justify-between p-3 bg-gray-700/50 rounded-lg">
                  <div className="flex items-center gap-3">
                    {getPaymentTypeIcon(payment.type)}
                    <div>
                      <p className="font-medium text-sm">{payment.customerName}</p>
                      <p className="text-xs text-gray-400">
                        {getPaymentTypeLabel(payment.type)} - {payment.orderNumber}
                      </p>
                      <p className="text-xs text-gray-500">{payment.submittedAt}</p>
                    </div>
                  </div>
                  <div className="text-left">
                    <p className="font-medium text-sm">{formatCurrency(payment.amount)}</p>
                    <div className="flex gap-1 mt-1">
                      <Button size="sm" variant="outline" className="h-6 w-6 p-0 border-green-500/50 text-green-400 hover:bg-green-500/20">
                        <CheckCircle className="h-3 w-3" />
                      </Button>
                      <Button size="sm" variant="outline" className="h-6 w-6 p-0 border-red-500/50 text-red-400 hover:bg-red-500/20">
                        <Trash2 className="h-3 w-3" />
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
              <Link href="/admin/payments/approve">
                <Button variant="outline" className="w-full mt-3 border-gray-600 text-gray-300 hover:bg-gray-700">
                  مشاهده همه ({stats.pendingPayments})
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card className="bg-gray-800 border-gray-700 text-white">
        <CardHeader>
          <CardTitle className="text-lg">فعالیت‌های اخیر</CardTitle>
          <CardDescription>آخرین اقدامات انجام شده در سیستم</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="flex items-center gap-3 p-3 bg-gray-700/30 rounded-lg">
              <CheckCircle className="h-5 w-5 text-green-400" />
              <div>
                <p className="text-sm">فیش پرداخت سفارش PRT-001 تأیید شد</p>
                <p className="text-xs text-gray-400">5 دقیقه پیش</p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 bg-gray-700/30 rounded-lg">
              <Users className="h-5 w-5 text-blue-400" />
              <div>
                <p className="text-sm">کاربر جدیدی در سیستم ثبت‌نام کرد</p>
                <p className="text-xs text-gray-400">15 دقیقه پیش</p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 bg-gray-700/30 rounded-lg">
              <DollarSign className="h-5 w-5 text-purple-400" />
              <div>
                <p className="text-sm">قیمت‌گذاری چاپ رنگی به‌روزرسانی شد</p>
                <p className="text-xs text-gray-400">1 ساعت پیش</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
