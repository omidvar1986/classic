'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import ProtectedRoute from '@/components/ProtectedRoute';
import AdminDashboardLayout from '@/components/admin/AdminDashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { 
  Save,
  Printer,
  DollarSign,
  Percent,
  FileText,
  Settings,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  Info
} from 'lucide-react';

interface PrintPriceSettings {
  basePricePerPage: number;
  colorPriceMultiplier: number;
  doubleSidedDiscount: number;
  a4Price: number;
  a3Price: number;
  a5Price: number;
  letterPrice: number;
  bulkDiscount10: number;
  bulkDiscount50: number;
  bulkDiscount100: number;
}

function PrintPricingContent() {
  const { user } = useAuth();
  const [settings, setSettings] = useState<PrintPriceSettings>({
    basePricePerPage: 5000,
    colorPriceMultiplier: 1.5,
    doubleSidedDiscount: 0.8,
    a4Price: 5000,
    a3Price: 10000,
    a5Price: 3000,
    letterPrice: 4500,
    bulkDiscount10: 0.95,
    bulkDiscount50: 0.90,
    bulkDiscount100: 0.85,
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);

  useEffect(() => {
    // Mock API call to fetch current settings
    setTimeout(() => {
      // In real app, this would be an API call
      setLoading(false);
    }, 1000);
  }, []);

  const handleInputChange = (field: keyof PrintPriceSettings, value: string) => {
    const numValue = parseFloat(value) || 0;
    setSettings(prev => ({
      ...prev,
      [field]: numValue
    }));
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      // Mock API call to save settings
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      console.log('Saving print pricing settings:', settings);
      setSaveMessage('تنظیمات قیمت‌گذاری با موفقیت ذخیره شد.');
      
      setTimeout(() => {
        setSaveMessage(null);
      }, 3000);
    } catch (error) {
      setSaveMessage('خطا در ذخیره تنظیمات. لطفاً دوباره تلاش کنید.');
    } finally {
      setSaving(false);
    }
  };

  const calculateSamplePrices = () => {
    const singlePageBW = settings.a4Price;
    const singlePageColor = Math.round(settings.a4Price * settings.colorPriceMultiplier);
    const doubleSidedBW = Math.round(singlePageBW * settings.doubleSidedDiscount);
    const doubleSidedColor = Math.round(singlePageColor * settings.doubleSidedDiscount);
    
    return {
      singlePageBW,
      singlePageColor,
      doubleSidedBW,
      doubleSidedColor,
      bulk10Pages: Math.round(singlePageBW * 10 * settings.bulkDiscount10),
      bulk50Pages: Math.round(singlePageBW * 50 * settings.bulkDiscount50),
      bulk100Pages: Math.round(singlePageBW * 100 * settings.bulkDiscount100),
    };
  };

  const samplePrices = calculateSamplePrices();

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
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="h-96 bg-gray-700 rounded"></div>
              <div className="h-96 bg-gray-700 rounded"></div>
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
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-white mb-2">قیمت‌گذاری خدمات چاپ</h2>
            <p className="text-gray-400">تنظیم قیمت‌ها و تخفیف‌های خدمات چاپ</p>
          </div>
          <div className="flex items-center gap-2">
            <Printer className="h-6 w-6 text-blue-400" />
            <DollarSign className="h-6 w-6 text-green-400" />
          </div>
        </div>

        {/* Save Message */}
        {saveMessage && (
          <Card className={`border-2 ${
            saveMessage.includes('موفقیت') 
              ? 'border-green-500/50 bg-green-500/10' 
              : 'border-red-500/50 bg-red-500/10'
          }`}>
            <CardContent className="p-4">
              <div className="flex items-center gap-2">
                {saveMessage.includes('موفقیت') 
                  ? <CheckCircle className="h-5 w-5 text-green-400" />
                  : <AlertCircle className="h-5 w-5 text-red-400" />
                }
                <span className={saveMessage.includes('موفقیت') ? 'text-green-400' : 'text-red-400'}>
                  {saveMessage}
                </span>
              </div>
            </CardContent>
          </Card>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Pricing Settings */}
          <div className="space-y-6">
            {/* Basic Pricing */}
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Settings className="h-5 w-5" />
                  قیمت‌گذاری پایه
                </CardTitle>
                <CardDescription>تنظیم قیمت‌های اساسی برای انواع چاپ</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label className="text-gray-300">قیمت پایه هر صفحه (تومان)</Label>
                  <Input
                    type="number"
                    value={settings.basePricePerPage}
                    onChange={(e) => handleInputChange('basePricePerPage', e.target.value)}
                    className="bg-gray-700 border-gray-600 text-white mt-1"
                    placeholder="5000"
                  />
                  <p className="text-xs text-gray-500 mt-1">قیمت پایه برای چاپ سیاه و سفید یک رو</p>
                </div>

                <div>
                  <Label className="text-gray-300">ضریب قیمت رنگی</Label>
                  <Input
                    type="number"
                    step="0.1"
                    value={settings.colorPriceMultiplier}
                    onChange={(e) => handleInputChange('colorPriceMultiplier', e.target.value)}
                    className="bg-gray-700 border-gray-600 text-white mt-1"
                    placeholder="1.5"
                  />
                  <p className="text-xs text-gray-500 mt-1">چند برابر گران‌تر از سیاه و سفید (مثلاً ۱.۵ = ۵۰٪ گران‌تر)</p>
                </div>

                <div>
                  <Label className="text-gray-300">تخفیف چاپ دو رو</Label>
                  <Input
                    type="number"
                    step="0.01"
                    value={settings.doubleSidedDiscount}
                    onChange={(e) => handleInputChange('doubleSidedDiscount', e.target.value)}
                    className="bg-gray-700 border-gray-600 text-white mt-1"
                    placeholder="0.8"
                  />
                  <p className="text-xs text-gray-500 mt-1">ضریب تخفیف برای چاپ دو رو (مثلاً ۰.۸ = ۲۰٪ تخفیف)</p>
                </div>
              </CardContent>
            </Card>

            {/* Paper Size Pricing */}
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <FileText className="h-5 w-5" />
                  قیمت‌گذاری بر اساس سایز کاغذ
                </CardTitle>
                <CardDescription>تنظیم قیمت برای هر سایز کاغذ</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className="text-gray-300">A4</Label>
                    <Input
                      type="number"
                      value={settings.a4Price}
                      onChange={(e) => handleInputChange('a4Price', e.target.value)}
                      className="bg-gray-700 border-gray-600 text-white mt-1"
                    />
                  </div>
                  <div>
                    <Label className="text-gray-300">A3</Label>
                    <Input
                      type="number"
                      value={settings.a3Price}
                      onChange={(e) => handleInputChange('a3Price', e.target.value)}
                      className="bg-gray-700 border-gray-600 text-white mt-1"
                    />
                  </div>
                  <div>
                    <Label className="text-gray-300">A5</Label>
                    <Input
                      type="number"
                      value={settings.a5Price}
                      onChange={(e) => handleInputChange('a5Price', e.target.value)}
                      className="bg-gray-700 border-gray-600 text-white mt-1"
                    />
                  </div>
                  <div>
                    <Label className="text-gray-300">Letter</Label>
                    <Input
                      type="number"
                      value={settings.letterPrice}
                      onChange={(e) => handleInputChange('letterPrice', e.target.value)}
                      className="bg-gray-700 border-gray-600 text-white mt-1"
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Bulk Discounts */}
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Percent className="h-5 w-5" />
                  تخفیف‌های عمده
                </CardTitle>
                <CardDescription>تنظیم تخفیف برای سفارشات پر حجم</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label className="text-gray-300">تخفیف ۱۰+ صفحه</Label>
                  <Input
                    type="number"
                    step="0.01"
                    value={settings.bulkDiscount10}
                    onChange={(e) => handleInputChange('bulkDiscount10', e.target.value)}
                    className="bg-gray-700 border-gray-600 text-white mt-1"
                  />
                  <p className="text-xs text-gray-500 mt-1">ضریب قیمت (مثلاً ۰.۹۵ = ۵٪ تخفیف)</p>
                </div>

                <div>
                  <Label className="text-gray-300">تخفیف ۵۰+ صفحه</Label>
                  <Input
                    type="number"
                    step="0.01"
                    value={settings.bulkDiscount50}
                    onChange={(e) => handleInputChange('bulkDiscount50', e.target.value)}
                    className="bg-gray-700 border-gray-600 text-white mt-1"
                  />
                  <p className="text-xs text-gray-500 mt-1">ضریب قیمت (مثلاً ۰.۹۰ = ۱۰٪ تخفیف)</p>
                </div>

                <div>
                  <Label className="text-gray-300">تخفیف ۱۰۰+ صفحه</Label>
                  <Input
                    type="number"
                    step="0.01"
                    value={settings.bulkDiscount100}
                    onChange={(e) => handleInputChange('bulkDiscount100', e.target.value)}
                    className="bg-gray-700 border-gray-600 text-white mt-1"
                  />
                  <p className="text-xs text-gray-500 mt-1">ضریب قیمت (مثلاً ۰.۸۵ = ۱۵٪ تخفیف)</p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Preview & Stats */}
          <div className="space-y-6">
            {/* Price Preview */}
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  پیش‌نمایش قیمت‌ها
                </CardTitle>
                <CardDescription>قیمت‌های نمونه بر اساس تنظیمات فعلی</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 gap-3">
                  <div className="flex justify-between items-center p-3 bg-gray-700/50 rounded-lg">
                    <span className="text-gray-300">یک صفحه سیاه و سفید</span>
                    <span className="font-medium text-white">{samplePrices.singlePageBW.toLocaleString('fa-IR')} تومان</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-gray-700/50 rounded-lg">
                    <span className="text-gray-300">یک صفحه رنگی</span>
                    <span className="font-medium text-white">{samplePrices.singlePageColor.toLocaleString('fa-IR')} تومان</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-gray-700/50 rounded-lg">
                    <span className="text-gray-300">یک صفحه دو رو سیاه و سفید</span>
                    <span className="font-medium text-white">{samplePrices.doubleSidedBW.toLocaleString('fa-IR')} تومان</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-gray-700/50 rounded-lg">
                    <span className="text-gray-300">یک صفحه دو رو رنگی</span>
                    <span className="font-medium text-white">{samplePrices.doubleSidedColor.toLocaleString('fa-IR')} تومان</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Bulk Pricing Preview */}
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Percent className="h-5 w-5" />
                  قیمت‌های عمده
                </CardTitle>
                <CardDescription>قیمت کل برای حجم‌های مختلف (سیاه و سفید)</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 gap-3">
                  <div className="flex justify-between items-center p-3 bg-gray-700/50 rounded-lg">
                    <span className="text-gray-300">۱۰ صفحه</span>
                    <div className="text-left">
                      <span className="font-medium text-white">{samplePrices.bulk10Pages.toLocaleString('fa-IR')} تومان</span>
                      <p className="text-xs text-green-400">
                        ۵٪ تخفیف (صرفه‌جویی: {(settings.a4Price * 10 - samplePrices.bulk10Pages).toLocaleString('fa-IR')} تومان)
                      </p>
                    </div>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-gray-700/50 rounded-lg">
                    <span className="text-gray-300">۵۰ صفحه</span>
                    <div className="text-left">
                      <span className="font-medium text-white">{samplePrices.bulk50Pages.toLocaleString('fa-IR')} تومان</span>
                      <p className="text-xs text-green-400">
                        ۱۰٪ تخفیف (صرفه‌جویی: {(settings.a4Price * 50 - samplePrices.bulk50Pages).toLocaleString('fa-IR')} تومان)
                      </p>
                    </div>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-gray-700/50 rounded-lg">
                    <span className="text-gray-300">۱۰۰ صفحه</span>
                    <div className="text-left">
                      <span className="font-medium text-white">{samplePrices.bulk100Pages.toLocaleString('fa-IR')} تومان</span>
                      <p className="text-xs text-green-400">
                        ۱۵٪ تخفیف (صرفه‌جویی: {(settings.a4Price * 100 - samplePrices.bulk100Pages).toLocaleString('fa-IR')} تومان)
                      </p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Info Card */}
            <Card className="bg-blue-900/20 border-blue-700/50">
              <CardContent className="p-4">
                <div className="flex items-start gap-3">
                  <Info className="h-5 w-5 text-blue-400 mt-0.5 flex-shrink-0" />
                  <div>
                    <h4 className="font-medium text-blue-400 mb-2">نکات مهم:</h4>
                    <ul className="text-sm text-blue-200 space-y-1">
                      <li>• تغییرات بلافاسله برای سفارشات جدید اعمال می‌شود</li>
                      <li>• قیمت‌های سفارشات در انتظار تغییر نمی‌کند</li>
                      <li>• تخفیف‌های عمده به‌صورت خودکار محاسبه می‌شود</li>
                      <li>• حتماً پس از تغییرات دکمه ذخیره را بزنید</li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Save Button */}
        <div className="flex justify-end pt-6 border-t border-gray-700">
          <Button
            onClick={handleSave}
            disabled={saving}
            className="bg-green-600 hover:bg-green-700 text-white px-8"
          >
            {saving ? (
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                در حال ذخیره...
              </div>
            ) : (
              <>
                <Save className="h-4 w-4 ml-2" />
                ذخیره تنظیمات
              </>
            )}
          </Button>
        </div>
      </div>
    </AdminDashboardLayout>
  );
}

export default function PrintPricingPage() {
  return (
    <ProtectedRoute>
      <PrintPricingContent />
    </ProtectedRoute>
  );
}
