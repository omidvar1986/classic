'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function NotFoundPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
      <div className="bg-white/10 border border-white/20 rounded-xl p-10 shadow-lg text-center max-w-lg">
        <h1 className="text-5xl font-bold text-white mb-4">404</h1>
        <h2 className="text-2xl font-semibold text-white mb-2">صفحه پیدا نشد</h2>
        <p className="text-gray-300 mb-8">متاسفانه صفحه مورد نظر شما وجود ندارد یا حذف شده است.</p>
        <Link href="/">
          <Button className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-medium px-8 py-3 text-lg">
            بازگشت به صفحه اصلی
          </Button>
        </Link>
      </div>
    </div>
  );
}