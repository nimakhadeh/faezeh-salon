"use client";

import { useState } from "react";
import Link from "next/link";
import { useAuth } from "@/lib/auth-context";
import { useRouter } from "next/navigation";
import { Scissors, Eye, EyeOff } from "lucide-react";
import toast, { Toaster } from "react-hot-toast";

export default function RegisterPage() {
  const { register } = useAuth();
  const router = useRouter();
  const [form, setForm] = useState({
    phone: "",
    username: "",
    first_name: "",
    last_name: "",
    password: "",
    password2: "",
    role: "customer",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.phone || !form.password || !form.first_name) {
      toast.error("لطفاً فیلدهای الزامی را پر کنید.");
      return;
    }
    if (form.password !== form.password2) {
      toast.error("رمز عبور و تکرار آن یکسان نیستند.");
      return;
    }
    setLoading(true);
    try {
      await register(form);
      toast.success("ثبت‌نام با موفقیت انجام شد!");
      router.push("/");
    } catch (err: any) {
      const msg = err.response?.data;
      if (typeof msg === "object") {
        toast.error(Object.values(msg).flat().join(" "));
      } else {
        toast.error("خطا در ثبت‌نام. لطفاً دوباره تلاش کنید.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-10">
      <Toaster position="top-center" />
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-2xl bg-rose-600 flex items-center justify-center mx-auto mb-4">
            <Scissors className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900">ثبت‌نام در سالن فائزه</h1>
          <p className="text-gray-500 mt-2">حساب کاربری جدید بسازید</p>
        </div>

        <div className="card">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">نام *</label>
                <input name="first_name" value={form.first_name} onChange={handleChange} className="input-field" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">نام خانوادگی</label>
                <input name="last_name" value={form.last_name} onChange={handleChange} className="input-field" />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">نام کاربری *</label>
              <input name="username" value={form.username} onChange={handleChange} className="input-field" dir="ltr" />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">شماره موبایل *</label>
              <input
                name="phone"
                type="tel"
                value={form.phone}
                onChange={handleChange}
                placeholder="۰۹۱۲۳۴۵۶۷۸۹"
                className="input-field text-left"
                dir="ltr"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">نقش</label>
              <select name="role" value={form.role} onChange={handleChange} className="input-field">
                <option value="customer">مشتری</option>
                <option value="specialist">متخصص</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">رمز عبور *</label>
              <div className="relative">
                <input
                  name="password"
                  type={showPassword ? "text" : "password"}
                  value={form.password}
                  onChange={handleChange}
                  className="input-field pl-10"
                />
                <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">تکرار رمز عبور *</label>
              <input
                name="password2"
                type="password"
                value={form.password2}
                onChange={handleChange}
                className="input-field"
              />
            </div>

            <button type="submit" disabled={loading} className="btn-primary w-full disabled:opacity-50">
              {loading ? "در حال ثبت‌نام..." : "ثبت‌نام"}
            </button>
          </form>

          <div className="mt-6 text-center text-sm text-gray-600">
            قبلاً ثبت‌نام کردید؟{" "}
            <Link href="/login" className="text-rose-600 hover:text-rose-700 font-medium">
              ورود
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
