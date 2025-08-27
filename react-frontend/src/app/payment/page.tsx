'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import ProtectedRoute from '@/components/ProtectedRoute';
import { 
  ArrowLeft,
  CreditCard,
  Upload,
  Copy,
  CheckCircle,
  AlertCircle,
  Banknote,
  User,
  Building
} from 'lucide-react';
import Link from 'next/link';
import { showToast } from '@/lib/utils';
import { digitalShopAPI } from '@/lib/api';

interface PaymentSettings {
  card_number: string;
  account_holder: string;
  bank_name: string;
  shaba_number?: string;
}

interface Order {
  id: number;
  order_number: string;
  total_amount: number;
  items: Array<{
    id: number;
    product_name: string;
    quantity: number;
    price: number;
  }>;
  customer_name: string;
  customer_phone: string;
  customer_address: string;
  customer_notes?: string;
  status: string;
  created_at: string;
}

function PaymentContent() {
  const { user } = useAuth();
  const [order, setOrder] = useState<Order | null>(null);
  const [paymentSettings, setPaymentSettings] = useState<PaymentSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [paymentReceipt, setPaymentReceipt] = useState<File | null>(null);
  const [paymentNotes, setPaymentNotes] = useState('');
  const [copiedField, setCopiedField] = useState<string | null>(null);

  useEffect(() => {
    // Get order from localStorage or URL params
    const orderData = localStorage.getItem('currentOrder');
    if (orderData) {
      setOrder(JSON.parse(orderData));
    }

    // Mock payment settings - in real app, fetch from API
    setPaymentSettings({
      card_number: '6037-1234-5678-9012',
      account_holder: 'فروشگاه دیجیتال کلاسیک',
      bank_name: 'بانک ملی ایران',
      shaba_number: 'IR123456789012345678901234'
    });

    setLoading(false);
  }, []);

  const copyToClipboard = async (text: string, field: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedField(field);
      setTimeout(() => setCopiedField(null), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setPaymentReceipt(file);
    }
  };

  const handleSubmitPayment = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!paymentReceipt) {
      showToast('لطفاً رسید پرداخت را آپلود کنید', 'error');
      return;
    }

    try {
      setUploading(true);
      
      if (!order) throw new Error('Order not found');
      const formData = new FormData();
      formData.append('receipt_image', paymentReceipt);
      formData.append('amount_paid', String(order.total_amount || ''));
      if (paymentNotes) formData.append('payment_notes', paymentNotes);
      await digitalShopAPI.uploadPaymentReceipt(order.id, formData);

      // Persist a local mirror for UX and offline visibility
      try {
        const orders = JSON.parse(localStorage.getItem('orders') || '[]');
        const idx = Array.isArray(orders) ? orders.findIndex((o: any) => o.id === order.id) : -1;
        if (idx !== -1) {
          orders[idx] = {
            ...orders[idx],
            status: 'pending_payment',
            payment_status: 'submitted',
          };
          localStorage.setItem('orders', JSON.stringify(orders));
        }
      } catch {}

      // Success toast and redirect
      showToast('پرداخت شما با موفقیت ثبت شد! در انتظار تایید مدیر.', 'success');
      localStorage.removeItem('currentOrder');
      window.location.href = '/shop-orders';
      
    } catch (error) {
      console.error('Error submitting payment:', error);
      showToast('خطا در ثبت پرداخت', 'error');
    } finally {
      setUploading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="text-white text-xl">در حال بارگذاری...</div>
      </div>
    );
  }

  if (!order) {
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
              <AlertCircle className="h-16 w-16 text-red-400 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-white mb-2">سفارش یافت نشد</h3>
              <p className="text-gray-300 mb-6">لطفاً ابتدا سفارش خود را تکمیل کنید</p>
              <Link href="/checkout">
                <Button className="bg-orange-600 hover:bg-orange-700 text-white">
                  تکمیل سفارش
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
          <Link href="/checkout">
            <Button variant="outline" className="border-white/20 text-white hover:bg-white/10">
              <ArrowLeft className="h-4 w-4 mr-2" />
              بازگشت به تکمیل سفارش
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold text-white">پرداخت سفارش</h1>
            <p className="text-gray-300">شماره سفارش: {order.order_number}</p>
          </div>
        </div>

        {/* Progress steps */}
        <div className="mb-6">
          <div className="flex items-center justify-center gap-4 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full bg-green-400"></div>
              <span className="text-green-300">سبد خرید</span>
            </div>
            <div className="w-8 h-px bg-white/20"></div>
            <div className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full bg-green-400"></div>
              <span className="text-green-300">تکمیل خرید</span>
            </div>
            <div className="w-8 h-px bg-white/20"></div>
            <div className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full bg-orange-400"></div>
              <span className="text-orange-300">پرداخت</span>
            </div>
            <div className="w-8 h-px bg-white/20"></div>
            <div className="flex items-center gap-2">
              <div className={`w-2.5 h-2.5 rounded-full ${paymentReceipt ? 'bg-blue-400' : 'bg-white/30'}`}></div>
              <span className={`${paymentReceipt ? 'text-blue-300' : 'text-gray-400'}`}>آپلود رسید</span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Payment Information */}
          <div className="lg:col-span-2 space-y-6">
            {/* Order Summary */}
            <Card className="bg-white/10 border-white/20">
              <CardHeader>
                <CardTitle className="text-white">خلاصه سفارش</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <p className="text-gray-400 text-sm">تاریخ سفارش:</p>
                    <p className="text-white">{new Date(order.created_at).toLocaleDateString('fa-IR')}</p>
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm">وضعیت:</p>
                    <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800">
                      در انتظار پرداخت
                    </span>
                  </div>
                </div>
                
                <div className="space-y-2">
                  {order.items.map((item) => (
                    <div key={item.id} className="flex justify-between items-center p-2 bg-white/5 rounded">
                      <div>
                        <span className="text-white">{item.product_name}</span>
                        <span className="text-gray-400 text-sm mr-2">({item.quantity} عدد)</span>
                      </div>
                      <span className="text-white font-semibold">
                        {(item.price * item.quantity).toLocaleString()} تومان
                      </span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Bank Information */}
            <Card className="bg-white/10 border-white/20">
              <CardHeader>
                <CardTitle className="text-white">اطلاعات پرداخت</CardTitle>
                <CardDescription className="text-gray-300">
                  لطفاً مبلغ دقیق سفارش را به شماره کارت زیر واریز کرده و رسید پرداخت را آپلود کنید
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Card Information */}
                  <div className="space-y-4">
                    <div>
                      <Label className="text-gray-300 text-sm">شماره کارت:</Label>
                      <div className="flex items-center gap-2 mt-1">
                        <div className="flex-1 p-3 bg-white/5 rounded border border-white/20">
                          <span className="text-white font-mono text-lg tracking-wider">
                            {paymentSettings?.card_number}
                          </span>
                        </div>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => copyToClipboard(paymentSettings?.card_number || '', 'card')}
                          className="border-white/20 text-white hover:bg-white/10"
                        >
                          {copiedField === 'card' ? <CheckCircle className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
                        </Button>
                      </div>
                    </div>

                    <div>
                      <Label className="text-gray-300 text-sm">صاحب حساب:</Label>
                      <div className="p-3 bg-white/5 rounded border border-white/20 mt-1">
                        <span className="text-white">{paymentSettings?.account_holder}</span>
                      </div>
                    </div>

                    <div>
                      <Label className="text-gray-300 text-sm">نام بانک:</Label>
                      <div className="p-3 bg-white/5 rounded border border-white/20 mt-1">
                        <span className="text-white">{paymentSettings?.bank_name}</span>
                      </div>
                    </div>

                    {paymentSettings?.shaba_number && (
                      <div>
                        <Label className="text-gray-300 text-sm">شماره شبا:</Label>
                        <div className="flex items-center gap-2 mt-1">
                          <div className="flex-1 p-3 bg-white/5 rounded border border-white/20">
                            <span className="text-white font-mono text-sm">
                              {paymentSettings.shaba_number}
                            </span>
                          </div>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => copyToClipboard(paymentSettings.shaba_number || '', 'shaba')}
                            className="border-white/20 text-white hover:bg-white/10"
                          >
                            {copiedField === 'shaba' ? <CheckCircle className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
                          </Button>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Payment Instructions */}
                  <div className="space-y-4">
                    <div className="bg-blue-500/20 border border-blue-500/30 rounded-lg p-4">
                      <h4 className="text-blue-400 font-semibold mb-2">دستورالعمل پرداخت:</h4>
                      <ol className="text-blue-300 text-sm space-y-2 list-decimal list-inside">
                        <li>مبلغ دقیق سفارش را به شماره کارت بالا واریز کنید</li>
                        <li>رسید پرداخت را در فرم سمت راست آپلود کنید</li>
                        <li>یادداشت پرداخت را وارد کنید (اختیاری)</li>
                        <li>روی "ثبت پرداخت" کلیک کنید</li>
                      </ol>
                    </div>

                    <div className="bg-green-500/20 border border-green-500/30 rounded-lg p-4">
                      <h4 className="text-green-400 font-semibold mb-2">نکات مهم:</h4>
                      <ul className="text-green-300 text-sm space-y-1 list-disc list-inside">
                        <li>فقط مبلغ دقیق سفارش را واریز کنید</li>
                        <li>رسید پرداخت باید واضح و خوانا باشد</li>
                        <li>پس از ثبت پرداخت، سفارش شما بررسی خواهد شد</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Payment Upload Form */}
          <div className="lg:col-span-1">
            <Card className="bg-white/10 border-white/20 sticky top-6">
              <CardHeader>
                <CardTitle className="text-white">آپلود رسید پرداخت</CardTitle>
                <CardDescription className="text-gray-300">
                  رسید پرداخت خود را آپلود کنید
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmitPayment} className="space-y-4">
                  {/* File Upload */}
                  <div>
                    <Label htmlFor="paymentReceipt" className="text-white">رسید پرداخت <span className="text-red-400">*</span></Label>
                    <div className="mt-2">
                      <div className="border-2 border-dashed border-white/20 rounded-lg p-6 text-center">
                        <Upload className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                        <div className="text-sm text-gray-400 mb-2">
                          {paymentReceipt ? paymentReceipt.name : 'فایل را اینجا بکشید یا کلیک کنید'}
                        </div>
                        <Input
                          id="paymentReceipt"
                          type="file"
                          accept="image/*,.pdf"
                          onChange={handleFileUpload}
                          className="hidden"
                        />
                        <Button
                          type="button"
                          variant="outline"
                          size="sm"
                          onClick={() => document.getElementById('paymentReceipt')?.click()}
                          className="border-white/20 text-white hover:bg-white/10"
                        >
                          انتخاب فایل
                        </Button>
                      </div>
                    </div>
                  </div>

                  {/* Payment Notes */}
                  <div>
                    <Label htmlFor="paymentNotes" className="text-white">یادداشت پرداخت (اختیاری)</Label>
                    <Textarea
                      id="paymentNotes"
                      value={paymentNotes}
                      onChange={(e) => setPaymentNotes(e.target.value)}
                      placeholder="یادداشت یا توضیحات اضافی خود را وارد کنید"
                      rows={3}
                      className="mt-2 bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                    />
                  </div>

                  {/* Submit Button */}
                  <Button
                    type="submit"
                    className="w-full bg-green-600 hover:bg-green-700 text-white"
                    disabled={!paymentReceipt || uploading}
                  >
                    {uploading ? (
                      <div className="flex items-center gap-2">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                        در حال ثبت پرداخت...
                      </div>
                    ) : (
                      <>
                        <CheckCircle className="h-4 w-4 mr-2" />
                        ثبت پرداخت
                      </>
                    )}
                  </Button>

                  <p className="text-gray-400 text-xs text-center">
                    با کلیک روی دکمه بالا، شما تأیید می‌کنید که پرداخت را انجام داده‌اید
                  </p>
                </form>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function PaymentPage() {
  return (
    <ProtectedRoute>
      <PaymentContent />
    </ProtectedRoute>
  );
}
