'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { GlowCard } from '@/components/ui/spotlight-card';
import { Mail, Lock, Eye, EyeOff } from 'lucide-react';
import Link from 'next/link';

const loginSchema = z.object({
  email: z.string().email('لطفا ایمیل معتبر وارد کنید'),
  password: z.string().min(6, 'رمز عبور باید حداقل 6 کاراکتر باشد'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export default function LoginPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();
  const router = useRouter();

  const form = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  });

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true);
    setError('');
    
    try {
      await login(data.email, data.password);
      router.push('/dashboard');
    } catch (error: any) {
      setError(error.message || 'خطا در ورود به سیستم');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4">
      <div className="w-full max-w-md">
        <GlowCard glowColor="purple" className="w-full">
          <Card className="border-0 bg-transparent shadow-none">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl font-bold text-white">
                ورود به سیستم
              </CardTitle>
              <CardDescription className="text-gray-300">
                حساب کاربری خود را وارد کنید
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                  <FormField
                    control={form.control}
                    name="email"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-white">ایمیل</FormLabel>
                        <FormControl>
                          <div className="relative">
                            <Mail className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                            <Input
                              {...field}
                              type="email"
                              placeholder="example@email.com"
                              className="pl-10 bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                            />
                          </div>
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  
                  <FormField
                    control={form.control}
                    name="password"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-white">رمز عبور</FormLabel>
                        <FormControl>
                          <div className="relative">
                            <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                            <Input
                              {...field}
                              type={showPassword ? 'text' : 'password'}
                              placeholder="رمز عبور خود را وارد کنید"
                              className="pl-10 pr-10 bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                            />
                            <button
                              type="button"
                              onClick={() => setShowPassword(!showPassword)}
                              className="absolute right-3 top-3 text-gray-400 hover:text-white"
                            >
                              {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                            </button>
                          </div>
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  
                  {error && (
                    <div className="text-red-400 text-sm text-center bg-red-400/10 p-3 rounded-lg">
                      {error}
                    </div>
                  )}
                  
                  <Button
                    type="submit"
                    className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-medium"
                    disabled={isLoading}
                  >
                    {isLoading ? 'در حال ورود...' : 'ورود'}
                  </Button>
                </form>
              </Form>
              
              <div className="mt-6 text-center">
                <p className="text-gray-300 text-sm">
                  حساب کاربری ندارید؟{' '}
                  <Link href="/register" className="text-purple-400 hover:text-purple-300 underline">
                    ثبت نام کنید
                  </Link>
                </p>
              </div>
            </CardContent>
          </Card>
        </GlowCard>
      </div>
    </div>
  );
} 