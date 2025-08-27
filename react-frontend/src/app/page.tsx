'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { GlowCard } from '@/components/ui/spotlight-card';
import { Button } from '@/components/ui/button';
import { Printer, Keyboard, ShoppingCart } from 'lucide-react';
import Link from 'next/link';

export default function HomePage() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      if (user) {
        router.push('/dashboard');
      }
    }
  }, [user, loading, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="text-white text-xl">در حال بارگذاری...</div>
      </div>
    );
  }

  if (user) {
    return null; // Will redirect to dashboard
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto text-center mb-16">
        <h1 className="text-5xl font-bold text-white mb-6">
          Smart Office
        </h1>
        <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
          سیستم جامع مدیریت خدمات چاپ، تایپ و فروشگاه دیجیتال
        </p>
        <div className="flex justify-center gap-4">
          <Link href="/login">
            <Button size="lg" className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-medium">
              ورود به سیستم
            </Button>
          </Link>
          <Link href="/register">
            <Button size="lg" variant="outline" className="border-white/20 text-white hover:bg-white/10">
              ثبت نام
            </Button>
          </Link>
        </div>
      </div>

      {/* Services Overview */}
      <div className="max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-white text-center mb-12">
          خدمات ما
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Print Service */}
          <GlowCard glowColor="green" size="lg">
            <div className="text-center">
              <Printer className="h-12 w-12 text-green-400 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-white mb-3">خدمات چاپ</h3>
              <p className="text-gray-300 mb-6">
                چاپ اسناد، تصاویر و فایل‌های مختلف با کیفیت بالا و قیمت مناسب
              </p>
              <Link href="/login">
                <Button className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-medium">
                  شروع کنید
                </Button>
              </Link>
            </div>
          </GlowCard>

          {/* Typing Service */}
          <GlowCard glowColor="purple" size="lg">
            <div className="text-center">
              <Keyboard className="h-12 w-12 text-purple-400 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-white mb-3">خدمات تایپ</h3>
              <p className="text-gray-300 mb-6">
                تایپ و ویرایش متون، اسناد و فایل‌های مختلف با دقت و سرعت بالا
              </p>
              <Link href="/login">
                <Button className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-medium">
                  شروع کنید
                </Button>
              </Link>
            </div>
          </GlowCard>

          {/* Digital Shop */}
          <GlowCard glowColor="orange" size="lg">
            <div className="text-center">
              <ShoppingCart className="h-12 w-12 text-orange-400 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-white mb-3">فروشگاه دیجیتال</h3>
              <p className="text-gray-300 mb-6">
                خرید لوازم التحریر، تجهیزات کامپیوتر و محصولات دیجیتال
              </p>
              <Link href="/login">
                <Button className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-medium">
                  شروع کنید
                </Button>
              </Link>
            </div>
          </GlowCard>
        </div>
      </div>

      {/* Footer */}
      <div className="max-w-7xl mx-auto mt-16 text-center">
        <p className="text-gray-400">
          © 2024 Smart Office. تمامی حقوق محفوظ است.
        </p>
      </div>
    </div>
  );
}
