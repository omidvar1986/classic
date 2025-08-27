'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { GlowCard } from '@/components/ui/spotlight-card';
import { Mail, Lock, Eye, EyeOff, User } from 'lucide-react';
import Link from 'next/link';

const registerSchema = z.object({
  first_name: z.string().min(2, 'نام باید حداقل 2 کاراکتر باشد'),
  last_name: z.string().min(2, 'نام خانوادگی باید حداقل 2 کاراکتر باشد'),
  email: z.string().email('لطفا ایمیل معتبر وارد کنید'),
  password: z.string().min(6, 'رمز عبور باید حداقل 6 کاراکتر باشد'),
  confirm_password: z.string(),
}).refine((data) => data.password === data.confirm_password, {
  message: "رمز عبور و تکرار آن یکسان نیستند",
  path: ["confirm_password"],
});

type RegisterFormData = z.infer<typeof registerSchema>;

export default function RegisterPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const { register } = useAuth();
  const router = useRouter();

  const form = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      first_name: '',
      last_name: '',
      email: '',
      password: '',
      confirm_password: '',
    },
  });

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true);
    setError('');
    
    try {
      await register({
        email: data.email,
        password: data.password,
        first_name: data.first_name,
        last_name: data.last_name,
      });
      router.push('/dashboard');
    } catch (error: any) {
      setError(error.message || 'خطا در ثبت نام');
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
                ثبت نام
              </CardTitle>
              <CardDescription className="text-gray-300">
                حساب کاربری جدید ایجاد کنید
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <FormField
                      control={form.control}
                      name="first_name"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="text-white">نام</FormLabel>
                          <FormControl>
                            <div className="relative">
                              <User className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                              <Input
                                {...field}
                                placeholder="نام"
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
                      name="last_name"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="text-white">نام خانوادگی</FormLabel>
                          <FormControl>
                            <div className="relative">
                              <User className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                              <Input
                                {...field}
                                placeholder="نام خانوادگی"
                                className="pl-10 bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                              />
                            </div>
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>
                  
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
                              placeholder="رمز عبور"
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
                  
                  <FormField
                    control={form.control}
                    name="confirm_password"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-white">تکرار رمز عبور</FormLabel>
                        <FormControl>
                          <div className="relative">
                            <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                            <Input
                              {...field}
                              type={showConfirmPassword ? 'text' : 'password'}
                              placeholder="تکرار رمز عبور"
                              className="pl-10 pr-10 bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                            />
                            <button
                              type="button"
                              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                              className="absolute right-3 top-3 text-gray-400 hover:text-white"
                            >
                              {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
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
                    {isLoading ? 'در حال ثبت نام...' : 'ثبت نام'}
                  </Button>
                </form>
              </Form>
              
              <div className="mt-6 text-center">
                <p className="text-gray-300 text-sm">
                  قبلاً حساب کاربری دارید؟{' '}
                  <Link href="/login" className="text-purple-400 hover:text-purple-300 underline">
                    وارد شوید
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