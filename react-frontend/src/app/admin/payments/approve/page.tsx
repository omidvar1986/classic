'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import ProtectedRoute from '@/components/ProtectedRoute';
import AdminDashboardLayout from '@/components/admin/AdminDashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { 
  CheckCircle, 
  XCircle, 
  Eye, 
  Search, 
  Filter,
  FileText,
  Edit,
  ShoppingCart,
  Calendar,
  Clock,
  User,
  DollarSign,
  Image as ImageIcon
} from 'lucide-react';

interface PaymentSlip {
  id: number;
  orderType: 'print' | 'typing' | 'shop';
  orderNumber: string;
  customerName: string;
  customerEmail: string;
  amount: number;
  submittedAt: string;
  status: 'pending' | 'approved' | 'rejected';
  paymentSlipImage: string;
  notes?: string;
}

function PaymentApprovalContent() {
  const { user } = useAuth();
  const [paymentSlips, setPaymentSlips] = useState<PaymentSlip[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('pending');
  const [typeFilter, setTypeFilter] = useState<string>('all');
  const [selectedSlip, setSelectedSlip] = useState<PaymentSlip | null>(null);

  useEffect(() => {
    // Mock data - replace with actual API call
    setTimeout(() => {
      setPaymentSlips([
        {
          id: 1,
          orderType: 'print',
          orderNumber: 'PRT-001',
          customerName: 'احمد محمدی',
          customerEmail: 'ahmad@example.com',
          amount: 45000,
          submittedAt: '1403/08/15 14:30',
          status: 'pending',
          paymentSlipImage: '/api/placeholder/400/600',
          notes: 'سفارش چاپ 10 صفحه رنگی A4'
        },
        {
          id: 2,
          orderType: 'typing',
          orderNumber: 'TYP-045',
          customerName: 'فاطمه احمدی',
          customerEmail: 'fatemeh@example.com',
          amount: 120000,
          submittedAt: '1403/08/15 12:15',
          status: 'pending',
          paymentSlipImage: '/api/placeholder/400/600',
          notes: 'تایپ سند 8 صفحه‌ای'
        },
        {
          id: 3,
          orderType: 'shop',
          orderNumber: 'SHP-234',
          customerName: 'علی رضایی',
          customerEmail: 'ali@example.com',
          amount: 350000,
          submittedAt: '1403/08/15 10:45',
          status: 'pending',
          paymentSlipImage: '/api/placeholder/400/600',
          notes: 'خرید لوازم التحریر'
        },
        {
          id: 4,
          orderType: 'print',
          orderNumber: 'PRT-002',
          customerName: 'مریم کریمی',
          customerEmail: 'maryam@example.com',
          amount: 25000,
          submittedAt: '1403/08/14 16:20',
          status: 'approved',
          paymentSlipImage: '/api/placeholder/400/600',
          notes: 'چاپ سیاه و سفید 5 صفحه'
        },
        {
          id: 5,
          orderType: 'typing',
          orderNumber: 'TYP-044',
          customerName: 'حسین موسوی',
          customerEmail: 'hossein@example.com',
          amount: 80000,
          submittedAt: '1403/08/14 11:10',
          status: 'rejected',
          paymentSlipImage: '/api/placeholder/400/600',
          notes: 'تایپ مقاله 5 صفحه‌ای - فیش پرداخت نامعتبر'
        },
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const handleApprove = async (slipId: number) => {
    // API call to approve payment slip
    console.log('Approving payment slip:', slipId);
    setPaymentSlips(prev => 
      prev.map(slip => 
        slip.id === slipId ? { ...slip, status: 'approved' as const } : slip
      )
    );
    setSelectedSlip(null);
  };

  const handleReject = async (slipId: number) => {
    // API call to reject payment slip
    console.log('Rejecting payment slip:', slipId);
    setPaymentSlips(prev => 
      prev.map(slip => 
        slip.id === slipId ? { ...slip, status: 'rejected' as const } : slip
      )
    );
    setSelectedSlip(null);
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'pending':
        return <Badge className="bg-yellow-500/20 text-yellow-400 hover:bg-yellow-500/30">منتظر بررسی</Badge>;
      case 'approved':
        return <Badge className="bg-green-500/20 text-green-400 hover:bg-green-500/30">تأیید شده</Badge>;
      case 'rejected':
        return <Badge className="bg-red-500/20 text-red-400 hover:bg-red-500/30">رد شده</Badge>;
      default:
        return <Badge variant="outline">نامشخص</Badge>;
    }
  };

  const getOrderTypeIcon = (type: string) => {
    switch (type) {
      case 'print':
        return <FileText className="h-4 w-4 text-blue-400" />;
      case 'typing':
        return <Edit className="h-4 w-4 text-purple-400" />;
      case 'shop':
        return <ShoppingCart className="h-4 w-4 text-green-400" />;
      default:
        return <FileText className="h-4 w-4" />;
    }
  };

  const getOrderTypeLabel = (type: string) => {
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

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('fa-IR').format(amount) + ' تومان';
  };

  const filteredSlips = paymentSlips.filter(slip => {
    const matchesSearch = slip.customerName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         slip.orderNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         slip.customerEmail.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || slip.status === statusFilter;
    const matchesType = typeFilter === 'all' || slip.orderType === typeFilter;
    return matchesSearch && matchesStatus && matchesType;
  });

  // Check if user is staff/admin
  if (!user?.is_staff && !user?.is_superuser) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-900 to-red-800">
        <div className="text-center p-8 bg-white/10 rounded-xl">
          <h1 className="text-2xl font-bold text-white mb-4">دسترسی محدود</h1>
          <p className="text-red-200">شما اجازه دسترسی به این بخش را ندارید.</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <AdminDashboardLayout>
        <div className="space-y-6">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-700 rounded w-64 mb-4"></div>
            <div className="grid gap-4">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="h-24 bg-gray-700 rounded"></div>
              ))}
            </div>
          </div>
        </div>
      </AdminDashboardLayout>
    );
  }

  return (
    <AdminDashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h2 className="text-2xl font-bold text-white mb-2">تأیید فیش‌های پرداخت</h2>
          <p className="text-gray-400">بررسی و تأیید فیش‌های پرداخت ارسال شده توسط کاربران</p>
        </div>

        {/* Filters */}
        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                  <Input
                    placeholder="جستجو در نام مشتری، شماره سفارش یا ایمیل..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="bg-gray-700 border-gray-600 text-white pr-10"
                  />
                </div>
              </div>
              <div className="flex gap-2">
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  className="px-3 py-2 bg-gray-700 border-gray-600 rounded-md text-white text-sm"
                >
                  <option value="all">همه وضعیت‌ها</option>
                  <option value="pending">منتظر بررسی</option>
                  <option value="approved">تأیید شده</option>
                  <option value="rejected">رد شده</option>
                </select>
                <select
                  value={typeFilter}
                  onChange={(e) => setTypeFilter(e.target.value)}
                  className="px-3 py-2 bg-gray-700 border-gray-600 rounded-md text-white text-sm"
                >
                  <option value="all">همه سرویس‌ها</option>
                  <option value="print">چاپ</option>
                  <option value="typing">تایپ</option>
                  <option value="shop">فروشگاه</option>
                </select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Payment Slips List */}
        <div className="grid gap-4">
          {filteredSlips.map((slip) => (
            <Card key={slip.id} className="bg-gray-800 border-gray-700">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    {getOrderTypeIcon(slip.orderType)}
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="text-lg font-medium text-white">{slip.customerName}</h3>
                        {getStatusBadge(slip.status)}
                      </div>
                      <div className="flex items-center gap-4 text-sm text-gray-400">
                        <span className="flex items-center gap-1">
                          <FileText className="h-3 w-3" />
                          {slip.orderNumber}
                        </span>
                        <span className="flex items-center gap-1">
                          <User className="h-3 w-3" />
                          {slip.customerEmail}
                        </span>
                        <span className="flex items-center gap-1">
                          <Calendar className="h-3 w-3" />
                          {slip.submittedAt}
                        </span>
                        <span className="flex items-center gap-1">
                          <DollarSign className="h-3 w-3" />
                          {formatCurrency(slip.amount)}
                        </span>
                      </div>
                      {slip.notes && (
                        <p className="text-sm text-gray-500 mt-1">{slip.notes}</p>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setSelectedSlip(slip)}
                      className="border-blue-500/50 text-blue-400 hover:bg-blue-500/20"
                    >
                      <Eye className="h-4 w-4 ml-1" />
                      مشاهده
                    </Button>
                    {slip.status === 'pending' && (
                      <>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleApprove(slip.id)}
                          className="border-green-500/50 text-green-400 hover:bg-green-500/20"
                        >
                          <CheckCircle className="h-4 w-4 ml-1" />
                          تأیید
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleReject(slip.id)}
                          className="border-red-500/50 text-red-400 hover:bg-red-500/20"
                        >
                          <XCircle className="h-4 w-4 ml-1" />
                          رد
                        </Button>
                      </>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredSlips.length === 0 && (
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-12 text-center">
              <FileText className="h-12 w-12 text-gray-600 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-white mb-2">فیش پرداختی یافت نشد</h3>
              <p className="text-gray-400">
                {searchTerm || statusFilter !== 'all' || typeFilter !== 'all' 
                  ? 'هیچ فیش پرداختی با فیلترهای اعمال شده پیدا نشد.'
                  : 'در حال حاضر فیش پرداختی برای بررسی وجود ندارد.'
                }
              </p>
            </CardContent>
          </Card>
        )}

        {/* Payment Slip Detail Modal */}
        {selectedSlip && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
            <Card className="bg-gray-800 border-gray-700 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <CardHeader className="border-b border-gray-700">
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-white">جزئیات فیش پرداخت</CardTitle>
                    <CardDescription>شماره سفارش: {selectedSlip.orderNumber}</CardDescription>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setSelectedSlip(null)}
                    className="border-gray-600"
                  >
                    بستن
                  </Button>
                </div>
              </CardHeader>
              <CardContent className="p-6">
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="text-sm text-gray-400">نام مشتری</label>
                      <p className="text-white font-medium">{selectedSlip.customerName}</p>
                    </div>
                    <div>
                      <label className="text-sm text-gray-400">ایمیل</label>
                      <p className="text-white font-medium">{selectedSlip.customerEmail}</p>
                    </div>
                    <div>
                      <label className="text-sm text-gray-400">نوع سفارش</label>
                      <div className="flex items-center gap-2 mt-1">
                        {getOrderTypeIcon(selectedSlip.orderType)}
                        <span className="text-white font-medium">{getOrderTypeLabel(selectedSlip.orderType)}</span>
                      </div>
                    </div>
                    <div>
                      <label className="text-sm text-gray-400">مبلغ</label>
                      <p className="text-white font-medium">{formatCurrency(selectedSlip.amount)}</p>
                    </div>
                    <div>
                      <label className="text-sm text-gray-400">تاریخ ارسال</label>
                      <p className="text-white font-medium">{selectedSlip.submittedAt}</p>
                    </div>
                    <div>
                      <label className="text-sm text-gray-400">وضعیت</label>
                      <div className="mt-1">{getStatusBadge(selectedSlip.status)}</div>
                    </div>
                  </div>
                  
                  {selectedSlip.notes && (
                    <div>
                      <label className="text-sm text-gray-400">توضیحات</label>
                      <p className="text-white">{selectedSlip.notes}</p>
                    </div>
                  )}

                  <div>
                    <label className="text-sm text-gray-400 mb-2 block">فیش پرداخت</label>
                    <div className="bg-gray-700 rounded-lg p-4">
                      <img
                        src={selectedSlip.paymentSlipImage}
                        alt="فیش پرداخت"
                        className="w-full max-w-md mx-auto rounded-lg"
                      />
                    </div>
                  </div>

                  {selectedSlip.status === 'pending' && (
                    <div className="flex gap-3 pt-4 border-t border-gray-700">
                      <Button
                        onClick={() => handleApprove(selectedSlip.id)}
                        className="flex-1 bg-green-600 hover:bg-green-700 text-white"
                      >
                        <CheckCircle className="h-4 w-4 ml-2" />
                        تأیید فیش پرداخت
                      </Button>
                      <Button
                        onClick={() => handleReject(selectedSlip.id)}
                        variant="outline"
                        className="flex-1 border-red-500/50 text-red-400 hover:bg-red-500/20"
                      >
                        <XCircle className="h-4 w-4 ml-2" />
                        رد فیش پرداخت
                      </Button>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </AdminDashboardLayout>
  );
}

export default function PaymentApprovalPage() {
  return (
    <ProtectedRoute>
      <PaymentApprovalContent />
    </ProtectedRoute>
  );
}
