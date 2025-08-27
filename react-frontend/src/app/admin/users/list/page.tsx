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
  Users, 
  Search, 
  Filter,
  Eye, 
  Edit, 
  Trash2,
  UserPlus,
  Shield,
  ShieldOff,
  Crown
} from 'lucide-react';

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_staff: boolean;
  is_superuser: boolean;
  is_active: boolean;
  date_joined: string;
  last_login: string;
}

function UserListContent() {
  const { user: currentUser } = useAuth();
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');

  useEffect(() => {
    // Mock data - replace with actual API call
    setTimeout(() => {
      setUsers([
        {
          id: 1,
          username: 'omidvar1334',
          email: 'omidvar1334@gmail.com',
          first_name: 'علی',
          last_name: 'امیدوار',
          is_staff: true,
          is_superuser: true,
          is_active: true,
          date_joined: '1403/08/01 10:30',
          last_login: '1403/08/15 14:30'
        },
        {
          id: 2,
          username: 'ahmad_user',
          email: 'ahmad@example.com',
          first_name: 'احمد',
          last_name: 'محمدی',
          is_staff: false,
          is_superuser: false,
          is_active: true,
          date_joined: '1403/08/05 12:15',
          last_login: '1403/08/14 16:20'
        },
        {
          id: 3,
          username: 'fatemeh_staff',
          email: 'fatemeh@example.com',
          first_name: 'فاطمه',
          last_name: 'احمدی',
          is_staff: true,
          is_superuser: false,
          is_active: true,
          date_joined: '1403/07/20 09:45',
          last_login: '1403/08/15 11:30'
        },
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const handleToggleStatus = (userId: number) => {
    setUsers(prev => 
      prev.map(user => 
        user.id === userId ? { ...user, is_active: !user.is_active } : user
      )
    );
  };

  const handleToggleStaff = (userId: number) => {
    setUsers(prev => 
      prev.map(user => 
        user.id === userId ? { ...user, is_staff: !user.is_staff } : user
      )
    );
  };

  const getStatusBadge = (user: User) => {
    if (!user.is_active) {
      return <Badge className="bg-gray-500/20 text-gray-400">غیرفعال</Badge>;
    }
    if (user.is_superuser) {
      return <Badge className="bg-yellow-500/20 text-yellow-400">مدیر ارشد</Badge>;
    }
    if (user.is_staff) {
      return <Badge className="bg-blue-500/20 text-blue-400">مدیر سیستم</Badge>;
    }
    return <Badge className="bg-green-500/20 text-green-400">کاربر عادی</Badge>;
  };

  const filteredUsers = users.filter(user => {
    const matchesSearch = user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.first_name.includes(searchTerm) ||
                         user.last_name.includes(searchTerm);
    
    const matchesFilter = 
      statusFilter === 'all' ||
      (statusFilter === 'active' && user.is_active) ||
      (statusFilter === 'inactive' && !user.is_active) ||
      (statusFilter === 'staff' && user.is_staff) ||
      (statusFilter === 'superuser' && user.is_superuser);
    
    return matchesSearch && matchesFilter;
  });

  // Check if user is staff/admin
  if (!currentUser?.is_staff && !currentUser?.is_superuser) {
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
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-white mb-2">مدیریت کاربران</h2>
            <p className="text-gray-400">مدیریت کاربران سیستم و دسترسی‌ها</p>
          </div>
          <Button className="bg-blue-600 hover:bg-blue-700 text-white">
            <UserPlus className="h-4 w-4 ml-2" />
            افزودن کاربر جدید
          </Button>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-white">{users.length}</div>
              <div className="text-sm text-gray-400">کل کاربران</div>
            </CardContent>
          </Card>
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-green-400">{users.filter(u => u.is_active).length}</div>
              <div className="text-sm text-gray-400">فعال</div>
            </CardContent>
          </Card>
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-blue-400">{users.filter(u => u.is_staff).length}</div>
              <div className="text-sm text-gray-400">مدیر سیستم</div>
            </CardContent>
          </Card>
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-yellow-400">{users.filter(u => u.is_superuser).length}</div>
              <div className="text-sm text-gray-400">مدیر ارشد</div>
            </CardContent>
          </Card>
        </div>

        {/* Filters */}
        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                  <Input
                    placeholder="جستجو در نام کاربری، ایمیل یا نام..."
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
                  <option value="all">همه کاربران</option>
                  <option value="active">فعال</option>
                  <option value="inactive">غیرفعال</option>
                  <option value="staff">مدیر سیستم</option>
                  <option value="superuser">مدیر ارشد</option>
                </select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Users List */}
        <div className="grid gap-4">
          {filteredUsers.map((user) => (
            <Card key={user.id} className="bg-gray-800 border-gray-700">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                      <span className="text-white font-medium">
                        {user.first_name?.charAt(0) || user.username?.charAt(0)}
                      </span>
                    </div>
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="text-lg font-medium text-white">
                          {user.first_name} {user.last_name}
                        </h3>
                        {getStatusBadge(user)}
                        {user.is_superuser && <Crown className="h-4 w-4 text-yellow-400" />}
                        {user.is_staff && !user.is_superuser && <Shield className="h-4 w-4 text-blue-400" />}
                      </div>
                      <div className="flex items-center gap-4 text-sm text-gray-400">
                        <span>@{user.username}</span>
                        <span>{user.email}</span>
                        <span>عضویت: {user.date_joined}</span>
                        <span>آخرین ورود: {user.last_login}</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      className="border-blue-500/50 text-blue-400 hover:bg-blue-500/20"
                    >
                      <Eye className="h-4 w-4 ml-1" />
                      مشاهده
                    </Button>
                    
                    {currentUser?.is_superuser && user.id !== currentUser?.id && (
                      <>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleToggleStaff(user.id)}
                          className={user.is_staff 
                            ? "border-orange-500/50 text-orange-400 hover:bg-orange-500/20"
                            : "border-green-500/50 text-green-400 hover:bg-green-500/20"
                          }
                        >
                          {user.is_staff ? <ShieldOff className="h-4 w-4 ml-1" /> : <Shield className="h-4 w-4 ml-1" />}
                          {user.is_staff ? 'لغو مدیریت' : 'مدیر کردن'}
                        </Button>
                        
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleToggleStatus(user.id)}
                          className={user.is_active 
                            ? "border-red-500/50 text-red-400 hover:bg-red-500/20"
                            : "border-green-500/50 text-green-400 hover:bg-green-500/20"
                          }
                        >
                          {user.is_active ? 'غیرفعال کردن' : 'فعال کردن'}
                        </Button>
                      </>
                    )}
                    
                    {user.id !== currentUser?.id && (
                      <Button
                        variant="outline"
                        size="sm"
                        className="border-red-500/50 text-red-400 hover:bg-red-500/20"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredUsers.length === 0 && (
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-12 text-center">
              <Users className="h-12 w-12 text-gray-600 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-white mb-2">کاربری یافت نشد</h3>
              <p className="text-gray-400">
                {searchTerm || statusFilter !== 'all' 
                  ? 'هیچ کاربری با فیلترهای اعمال شده پیدا نشد.'
                  : 'در حال حاضر کاربری در سیستم وجود ندارد.'
                }
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </AdminDashboardLayout>
  );
}

export default function UserListPage() {
  return (
    <ProtectedRoute>
      <UserListContent />
    </ProtectedRoute>
  );
}
