'use client';

import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  CreditCard,
  Users,
  Settings,
  Package,
  ShoppingBag,
  FileText,
  Building2,
  Menu,
  X,
  LogOut,
  ChevronDown,
  Printer,
  Keyboard,
  DollarSign,
  CheckCircle,
  UserCog,
  Wrench
} from 'lucide-react';

interface AdminDashboardLayoutProps {
  children: React.ReactNode;
}

interface NavItem {
  name: string;
  href: string;
  icon: React.ComponentType<any>;
  children?: NavItem[];
}

const navigation: NavItem[] = [
  {
    name: 'داشبورد',
    href: '/admin',
    icon: LayoutDashboard,
  },
  {
    name: 'مدیریت پرداخت‌ها',
    href: '/admin/payments',
    icon: CreditCard,
    children: [
      {
        name: 'تأیید فیش‌های پرداخت',
        href: '/admin/payments/approve',
        icon: CheckCircle,
      },
      {
        name: 'تنظیمات پرداخت',
        href: '/admin/payments/settings',
        icon: Settings,
      },
    ]
  },
  {
    name: 'مدیریت کاربران',
    href: '/admin/users',
    icon: Users,
    children: [
      {
        name: 'لیست کاربران',
        href: '/admin/users/list',
        icon: Users,
      },
      {
        name: 'آمار کاربران',
        href: '/admin/users/statistics',
        icon: UserCog,
      },
    ]
  },
  {
    name: 'مدیریت قیمت‌ها',
    href: '/admin/pricing',
    icon: DollarSign,
    children: [
      {
        name: 'قیمت‌گذاری چاپ',
        href: '/admin/pricing/print',
        icon: Printer,
      },
      {
        name: 'قیمت‌گذاری تایپ',
        href: '/admin/pricing/typing',
        icon: Keyboard,
      },
    ]
  },
  {
    name: 'لوازم جانبی',
    href: '/admin/accessories',
    icon: Package,
    children: [
      {
        name: 'مدیریت لوازم جانبی',
        href: '/admin/accessories/manage',
        icon: Package,
      },
      {
        name: 'پکیج‌های تخفیف',
        href: '/admin/accessories/packages',
        icon: Wrench,
      },
    ]
  },
  {
    name: 'فروشگاه دیجیتال',
    href: '/admin/shop',
    icon: ShoppingBag,
    children: [
      {
        name: 'محصولات',
        href: '/admin/shop/products',
        icon: Package,
      },
      {
        name: 'سفارشات',
        href: '/admin/shop/orders',
        icon: FileText,
      },
      {
        name: 'دسته‌بندی‌ها',
        href: '/admin/shop/categories',
        icon: Wrench,
      },
    ]
  },
  {
    name: 'خدمات دولتی',
    href: '/admin/government',
    icon: Building2,
    children: [
      {
        name: 'درخواست‌ها',
        href: '/admin/government/requests',
        icon: FileText,
      },
      {
        name: 'خدمات',
        href: '/admin/government/services',
        icon: Building2,
      },
    ]
  },
];

export default function AdminDashboardLayout({ children }: AdminDashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [expandedItems, setExpandedItems] = useState<Record<string, boolean>>({});
  const pathname = usePathname();
  const { user, logout } = useAuth();

  const toggleExpand = (href: string) => {
    setExpandedItems(prev => ({
      ...prev,
      [href]: !prev[href]
    }));
  };

  const handleLogout = async () => {
    await logout();
  };

  const isActive = (href: string) => {
    if (href === '/admin') {
      return pathname === '/admin';
    }
    return pathname.startsWith(href);
  };

  const NavItemComponent = ({ item, level = 0 }: { item: NavItem; level?: number }) => {
    const hasChildren = item.children && item.children.length > 0;
    const isExpanded = expandedItems[item.href];
    const active = isActive(item.href);

    return (
      <div key={item.href}>
        <div
          className={`flex items-center justify-between p-3 rounded-lg transition-colors cursor-pointer ${
            active
              ? 'bg-blue-600 text-white'
              : 'text-gray-300 hover:bg-gray-700 hover:text-white'
          } ${level > 0 ? 'mr-4' : ''}`}
          onClick={() => hasChildren ? toggleExpand(item.href) : null}
        >
          <Link 
            href={hasChildren ? '#' : item.href}
            className="flex items-center flex-1"
            onClick={(e) => hasChildren && e.preventDefault()}
          >
            <item.icon className="h-5 w-5 ml-3" />
            <span className="text-sm font-medium">{item.name}</span>
          </Link>
          {hasChildren && (
            <ChevronDown 
              className={`h-4 w-4 transition-transform ${
                isExpanded ? 'rotate-180' : ''
              }`}
            />
          )}
        </div>
        
        {hasChildren && isExpanded && (
          <div className="mt-1 space-y-1">
            {item.children!.map((child) => (
              <NavItemComponent key={child.href} item={child} level={level + 1} />
            ))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-20 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`fixed inset-y-0 right-0 z-30 w-80 bg-gray-800 transform transition-transform lg:translate-x-0 lg:static lg:inset-0 ${
        sidebarOpen ? 'translate-x-0' : 'translate-x-full'
      }`}>
        <div className="flex items-center justify-between h-16 px-4 border-b border-gray-700">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded"></div>
            </div>
            <div className="mr-3">
              <div className="text-white font-medium">پنل مدیریت</div>
              <div className="text-gray-400 text-xs">سیستم هوشمند اداری</div>
            </div>
          </div>
          <button 
            onClick={() => setSidebarOpen(false)}
            className="lg:hidden text-gray-400 hover:text-white"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        {/* User info */}
        <div className="p-4 border-b border-gray-700">
          <div className="flex items-center">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
              <span className="text-white font-medium text-sm">
                {user?.first_name?.charAt(0) || user?.username?.charAt(0) || 'A'}
              </span>
            </div>
            <div className="mr-3">
              <div className="text-white font-medium text-sm">
                {user?.first_name || user?.username}
              </div>
              <div className="text-gray-400 text-xs">
                {user?.is_superuser ? 'مدیر ارشد' : 'مدیر سیستم'}
              </div>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="mt-4 px-4 pb-4 space-y-2 flex-1 overflow-y-auto">
          {navigation.map((item) => (
            <NavItemComponent key={item.href} item={item} />
          ))}
        </nav>

        {/* Logout */}
        <div className="p-4 border-t border-gray-700">
          <Button
            onClick={handleLogout}
            variant="outline"
            className="w-full border-red-500/50 text-red-400 hover:bg-red-500/20 hover:text-red-300"
          >
            <LogOut className="h-4 w-4 ml-2" />
            خروج از سیستم
          </Button>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:mr-80">
        {/* Top header */}
        <header className="bg-gray-800 shadow-lg lg:shadow-none">
          <div className="px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <div className="flex items-center">
                <button
                  onClick={() => setSidebarOpen(true)}
                  className="lg:hidden text-gray-400 hover:text-white"
                >
                  <Menu className="h-6 w-6" />
                </button>
                <h1 className="text-white text-lg font-medium mr-4 lg:mr-0">
                  پنل مدیریت سیستم
                </h1>
              </div>
              
              {/* Back to Dashboard Button */}
              <div className="flex items-center gap-3">
                <Link href="/dashboard">
                  <Button variant="outline" className="border-white/20 text-white hover:bg-white/10">
                    <LayoutDashboard className="h-4 w-4 ml-2" />
                    بازگشت به داشبورد
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="py-6">
          <div className="px-4 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
