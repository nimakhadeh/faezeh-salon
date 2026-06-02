"use client";

import { useState } from "react";
import Link from "next/link";
import { authApi } from "@/lib/api";
import { Scissors, ArrowLeft } from "lucide-react";
import toast, { Toaster } from "react-hot-toast";

export default function ForgotPasswordPage() {
  const [step, setStep] = useState<"request" | "verify">("request");
  const [phone, setPhone] = useState("");
  const [code, setCode] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRequest = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await authApi.requestOTP(phone);
      toast.success("کد تأیید ارسال شد.");
      setStep("verify");
    } catch {
      toast.error("خطا در ارسال کد.");
    } finally {
      setLoading(false);
    }
  };

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await authApi.verifyOTP({ phone, code, new_password: newPassword });
      toast.success("رمز عبور با موفقیت تغییر کرد!");
      window.location.href = "/login";
    } catch {
      toast.error("کد نامعتبر است.");
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
          <h1 className="text-2xl font-bold text-gray-900">بازنشانی رمز عبور</h1>
        </div>

        <div className="card">
          {step === "request" ? (
            <form onSubmit={handleRequest} className="space-y-4">
              <p className="text-sm text-gray-600">شماره موبایل خود را وارد کنید تا کد تأیید ارسال شود.</p>
              <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="۰۹۱۲۳۴۵۶۷۸۹"
                className="input-field text-left"
                dir="ltr"
              />
              <button type="submit" disabled={loading} className="btn-primary w-full">
                {loading ? "..." : "ارسال کد"}
              </button>
            </form>
          ) : (
            <form onSubmit={handleVerify} className="space-y-4">
              <input
                type="text"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="کد ۶ رقمی"
                className="input-field text-center tracking-[1em]"
                maxLength={6}
              />
              <input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="رمز عبور جدید"
                className="input-field"
              />
              <button type="submit" disabled={loading} className="btn-primary w-full">
                {loading ? "..." : "تغییر رمز"}
              </button>
            </form>
          )}

          <Link href="/login" className="flex items-center gap-2 text-rose-600 text-sm mt-6 justify-center">
            <ArrowLeft className="w-4 h-4" />
            بازگشت به ورود
          </Link>
        </div>
      </div>
    </div>
  );
}
