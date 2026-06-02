"use client";

import { useState } from "react";
import Link from "next/link";
import { useAuth } from "@/lib/auth-context";
import { useRouter } from "next/navigation";
import { Scissors, Eye, EyeOff } from "lucide-react";
import toast, { Toaster } from "react-hot-toast";

export default function LoginPage() {
  const { login } = useAuth();
  const router = useRouter();
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!phone || !password) {
      toast.error("لطفاً همه فیلدها را پر کنید.");
      return;
    }
    setLoading(true);
    try {
      await login(phone, password);
      toast.success("ورود با موفقیت انجام شد!");
      router.push("/");
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "شماره موبایل یا رمز عبور اشتباه است.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <Toaster position="top-center" />
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-2xl bg-rose-600 flex items-center justify-center mx-auto mb-4">
            <Scissors className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900">ورود به سالن فائزه</h1>
          <p className="text-gray-500 mt-2">به حساب کاربری خود وارد شوید</p>
        </div>

        <div className="card">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                شماره موبایل
              </label>
              <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="۰۹۱۲۳۴۵۶۷۸۹"
                className="input-field text-left"
                dir="ltr"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                رمز عبور
              </label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="رمز عبور"
                  className="input-field pl-10"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            <div className="flex justify-between items-center text-sm">
              <Link href="/forgot-password" className="text-rose-600 hover:text-rose-700">
                رمز عبور را فراموش کردید؟
              </Link>
            </div>

            <button type="submit" disabled={loading} className="btn-primary w-full disabled:opacity-50">
              {loading ? "در حال ورود..." : "ورود"}
            </button>
          </form>

          <div className="mt-6 text-center text-sm text-gray-600">
            حساب کاربری ندارید؟{" "}
            <Link href="/register" className="text-rose-600 hover:text-rose-700 font-medium">
              ثبت‌نام
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
