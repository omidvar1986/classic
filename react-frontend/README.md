# Smart Office React Frontend

این پروژه یک رابط کاربری React برای سیستم مدیریت خدمات Smart Office است که شامل خدمات چاپ، تایپ و فروشگاه دیجیتال می‌باشد.

## ویژگی‌ها

- 🔐 **احراز هویت کامل**: ورود، ثبت نام و مدیریت جلسه کاربر
- 🎨 **طراحی مدرن**: استفاده از shadcn/ui و Tailwind CSS
- ✨ **کارت‌های درخشان**: کامپوننت Spotlight Card با افکت‌های تعاملی
- 📱 **واکنش‌گرا**: طراحی سازگار با تمام دستگاه‌ها
- 🔄 **مدیریت حالت**: استفاده از React Context برای مدیریت وضعیت کاربر
- 🌐 **API Integration**: اتصال کامل به Django Backend

## تکنولوژی‌های استفاده شده

- **Next.js 14** - فریم‌ورک React
- **TypeScript** - زبان برنامه‌نویسی
- **Tailwind CSS** - فریم‌ورک CSS
- **shadcn/ui** - کامپوننت‌های UI
- **React Hook Form** - مدیریت فرم‌ها
- **Zod** - اعتبارسنجی داده‌ها
- **Axios** - درخواست‌های HTTP
- **Lucide React** - آیکون‌ها

## نصب و راه‌اندازی

### پیش‌نیازها

- Node.js 18+ 
- npm یا yarn
- Django Backend (Smart Office)

### مراحل نصب

1. **کلون کردن پروژه**:
```bash
cd react-frontend
```

2. **نصب وابستگی‌ها**:
```bash
npm install
```

3. **تنظیم متغیرهای محیطی**:
فایل `.env.local` را در پوشه اصلی پروژه ایجاد کنید:
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

4. **اجرای پروژه**:
```bash
npm run dev
```

پروژه در آدرس `http://localhost:3000` در دسترس خواهد بود.

## ساختار پروژه

```
src/
├── app/                    # صفحات Next.js App Router
│   ├── dashboard/         # داشبورد کاربر
│   ├── login/            # صفحه ورود
│   └── page.tsx          # صفحه اصلی
├── components/
│   ├── ui/               # کامپوننت‌های shadcn/ui
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   ├── form.tsx
│   │   └── spotlight-card.tsx  # کامپوننت اصلی
│   └── ProtectedRoute.tsx      # محافظت از مسیرها
├── contexts/
│   └── AuthContext.tsx   # مدیریت احراز هویت
└── lib/
    ├── api.ts            # سرویس‌های API
    └── utils.ts          # توابع کمکی
```

## کامپوننت Spotlight Card

کامپوننت اصلی پروژه که افکت‌های درخشان تعاملی را فراهم می‌کند:

### ویژگی‌ها:
- **رنگ‌های مختلف**: آبی، بنفش، سبز، قرمز، نارنجی
- **اندازه‌های مختلف**: کوچک، متوسط، بزرگ
- **اندازه سفارشی**: امکان تعریف اندازه دلخواه
- **تعامل با موس**: افکت‌های درخشان بر اساس موقعیت موس

### استفاده:
```tsx
import { GlowCard } from '@/components/ui/spotlight-card';

<GlowCard glowColor="purple" size="lg">
  <div>محتوای کارت</div>
</GlowCard>
```

## API Integration

پروژه به Django Backend متصل می‌شود و شامل سرویس‌های زیر است:

### احراز هویت:
- `authAPI.login()` - ورود کاربر
- `authAPI.register()` - ثبت نام کاربر
- `authAPI.logout()` - خروج کاربر
- `authAPI.getProfile()` - دریافت اطلاعات پروفایل

### داشبورد:
- `dashboardAPI.getDashboard()` - اطلاعات کلی داشبورد
- `dashboardAPI.getPrintOrders()` - سفارشات چاپ
- `dashboardAPI.getTypingOrders()` - سفارشات تایپ
- `dashboardAPI.getDigitalShopOrders()` - سفارشات فروشگاه

### خدمات:
- `printServiceAPI` - API خدمات چاپ
- `typingServiceAPI` - API خدمات تایپ
- `digitalShopAPI` - API فروشگاه دیجیتال

## صفحات اصلی

### 1. صفحه اصلی (`/`)
- معرفی خدمات
- دکمه‌های ورود و ثبت نام
- نمایش کارت‌های درخشان خدمات

### 2. صفحه ورود (`/login`)
- فرم ورود با اعتبارسنجی
- نمایش خطاها
- لینک به صفحه ثبت نام

### 3. داشبورد (`/dashboard`)
- آمار کلی سفارشات
- کارت‌های درخشان برای هر سرویس
- دسترسی سریع به بخش‌های مختلف
- اطلاعات کاربر و دکمه خروج

## مدیریت احراز هویت

پروژه از React Context برای مدیریت وضعیت کاربر استفاده می‌کند:

```tsx
import { useAuth } from '@/contexts/AuthContext';

const { user, login, logout, loading } = useAuth();
```

### ویژگی‌ها:
- **مدیریت خودکار توکن**: ذخیره و حذف خودکار توکن احراز هویت
- **بررسی خودکار**: بررسی وضعیت احراز هویت در بارگذاری
- **محافظت از مسیرها**: کامپوننت `ProtectedRoute` برای محافظت از صفحات

## استایل‌دهی

پروژه از Tailwind CSS برای استایل‌دهی استفاده می‌کند:

### تم رنگی:
- **پس‌زمینه**: گرادیان آبی-بنفش
- **کارت‌ها**: شفاف با افکت‌های درخشان
- **متن**: سفید و خاکستری
- **دکمه‌ها**: رنگ‌های مختلف برای هر سرویس

### کلاس‌های مهم:
```css
bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900
bg-white/10 border-white/20
text-white text-gray-300
```

## توسعه

### اضافه کردن کامپوننت جدید:
```bash
npx shadcn@latest add [component-name]
```

### اجرای تست‌ها:
```bash
npm run test
```

### ساخت برای تولید:
```bash
npm run build
npm start
```

## نکات مهم

1. **CORS**: Django Backend باید CORS را برای `http://localhost:3000` فعال کند
2. **توکن**: توکن احراز هویت در localStorage ذخیره می‌شود
3. **RTL**: پروژه برای زبان فارسی و RTL بهینه شده است
4. **Responsive**: تمام صفحات واکنش‌گرا هستند

## پشتیبانی

برای سوالات و مشکلات، لطفاً با تیم توسعه تماس بگیرید.

---

**Smart Office React Frontend** - نسخه 1.0.0
