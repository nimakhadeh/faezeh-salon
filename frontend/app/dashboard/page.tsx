"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth-context";
import { useRouter } from "next/navigation";
import { appointmentsApi, walletApi, loyaltyApi, paymentsApi } from "@/lib/api";
import Navbar from "@/components/navbar";
import Footer from "@/components/footer";
import {
  Calendar, Wallet, Star, Clock, ArrowLeft,
  CheckCircle, XCircle, CreditCard, Gift,
} from "lucide-react";
import { formatPrice, getStatusLabel, getStatusColor } from "@/lib/utils";
import toast, { Toaster } from "react-hot-toast";

export default function DashboardPage() {
  const { user, isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const [appointments, setAppointments] = useState<any[]>([]);
  const [wallet, setWallet] = useState<any>(null);
  const [loyalty, setLoyalty] = useState<any>(null);
  const [transactions, setTransactions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("appointments");

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isLoading, isAuthenticated]);

  useEffect(() => {
    if (isAuthenticated) {
      fetchData();
    }
  }, [isAuthenticated]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [apptRes, walletRes, loyaltyRes, txRes] = await Promise.all([
        appointmentsApi.my(),
        walletApi.detail().catch(() => ({ data: null })),
        loyaltyApi.my().catch(() => ({ data: null })),
        paymentsApi.transactions().catch(() => ({ data: { results: [] } })),
      ]);
      setAppointments(apptRes.data || []);
      setWallet(walletRes.data);
      setLoyalty(loyaltyRes.data);
      setTransactions(txRes.data.results || txRes.data || []);
    } catch {
      toast.error("خطا در بارگذاری داده‌ها");
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = async (id: number) => {
    try {
      await appointmentsApi.cancel(id);
      toast.success("نوبت لغو شد");
      fetchData();
    } catch {
      toast.error("خطا در لغو نوبت");
    }
  };

  if (isLoading) return <div className="text-center py-20">در حال بارگذاری...</div>;
  if (!isAuthenticated) return null;

  const tabs = [
    { key: "appointments", label: "نوبت‌ها", icon: Calendar },
    { key: "wallet", label: "کیف پول", icon: Wallet },
    { key: "loyalty", label: "امتیازات", icon: Gift },
    { key: "transactions", label: "تراکنش‌ها", icon: CreditCard },
  ];

  const upcoming = appointments.filter((a) => a.status === "confirmed" || a.status === "deposit_paid");
  const past = appointments.filter((a) => a.status === "completed" || a.status === "canceled");

  return (
    <div className="min-h-screen bg-gray-50">
      <Toaster position="top-center" />
      <Navbar />

      <div className="bg-gradient-to-br from-rose-50 to-pink-50 py-10">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-rose-600 flex items-center justify-center text-white text-2xl font-bold">
              {user?.first_name?.[0] || "U"}
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                {user?.first_name} {user?.last_name}
              </h1>
              <p className="text-gray-600" dir="ltr">{user?.phone}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Stats */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div className="card text-center">
            <Calendar className="w-8 h-8 text-rose-600 mx-auto mb-2" />
            <div className="text-2xl font-bold">{appointments.length}</div>
            <div className="text-sm text-gray-500">کل نوبت‌ها</div>
          </div>
          <div className="card text-center">
            <Wallet className="w-8 h-8 text-green-600 mx-auto mb-2" />
            <div className="text-2xl font-bold">{formatPrice(wallet?.balance || 0)}</div>
            <div className="text-sm text-gray-500">موجودی (تومان)</div>
          </div>
          <div className="card text-center">
            <Gift className="w-8 h-8 text-amber-600 mx-auto mb-2" />
            <div className="text-2xl font-bold">{loyalty?.points || 0}</div>
            <div className="text-sm text-gray-500">امتیاز وفاداری</div>
          </div>
          <div className="card text-center">
            <Star className="w-8 h-8 text-purple-600 mx-auto mb-2" />
            <div className="text-2xl font-bold">{upcoming.length}</div>
            <div className="text-sm text-gray-500">نوبت پیش‌رو</div>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
          {tabs.map((t) => (
            <button
              key={t.key}
              onClick={() => setActiveTab(t.key)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-colors ${
                activeTab === t.key
                  ? "bg-rose-600 text-white"
                  : "bg-white text-gray-600 hover:bg-gray-50 border border-gray-200"
              }`}
            >
              <t.icon className="w-4 h-4" />
              {t.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        {activeTab === "appointments" && (
          <div>
            <h2 className="section-title text-lg">نوبت‌های پیش‌رو</h2>
            {upcoming.length === 0 ? (
              <div className="card text-center py-8 text-gray-400">
                <Calendar className="w-12 h-12 mx-auto mb-3" />
                نوبت فعالی ندارید
              </div>
            ) : (
              <div className="space-y-3 mb-8">
                {upcoming.map((a) => (
                  <div key={a.id} className="card flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="font-bold">{a.service_name}</h3>
                        <span className={`text-xs px-2 py-0.5 rounded-full ${getStatusColor(a.status)}`}>
                          {getStatusLabel(a.status)}
                        </span>
                      </div>
                      <p className="text-sm text-gray-500">
                        {a.date} - {a.start_time} | متخصص: {a.specialist_name}
                      </p>
                    </div>
                    <div className="flex gap-2">
                      {a.can_cancel && (
                        <button
                          onClick={() => handleCancel(a.id)}
                          className="text-red-500 hover:bg-red-50 px-3 py-1.5 rounded-lg text-sm transition-colors"
                        >
                          لغو
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}

            <h2 className="section-title text-lg">تاریخچه نوبت‌ها</h2>
            {past.length === 0 ? (
              <div className="card text-center py-8 text-gray-400">تاریخچه خالی</div>
            ) : (
              <div className="space-y-3">
                {past.map((a) => (
                  <div key={a.id} className="card opacity-75">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="font-medium">{a.service_name}</h3>
                      <span className={`text-xs px-2 py-0.5 rounded-full ${getStatusColor(a.status)}`}>
                        {getStatusLabel(a.status)}
                      </span>
                    </div>
                    <p className="text-sm text-gray-500">{a.date} - {a.start_time}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === "wallet" && (
          <div className="card">
            <div className="flex justify-between items-center mb-6">
              <div>
                <p className="text-sm text-gray-500">موجودی فعلی</p>
                <p className="text-3xl font-bold text-gray-900">{formatPrice(wallet?.balance || 0)} تومان</p>
              </div>
              <button className="btn-primary">شارژ کیف پول</button>
            </div>
            <div className="border-t pt-4">
              <p className="text-sm text-gray-500">برای پرداخت نوبت و خرید محصولات از کیف پول خود استفاده کنید.</p>
            </div>
          </div>
        )}

        {activeTab === "loyalty" && (
          <div className="card">
            <div className="text-center mb-6">
              <Gift className="w-12 h-12 text-amber-500 mx-auto mb-3" />
              <p className="text-3xl font-bold text-gray-900">{loyalty?.points || 0} امتیاز</p>
              <p className="text-sm text-gray-500 mt-1">
                کل امتیاز کسب شده: {loyalty?.total_earned || 0} | مصرف شده: {loyalty?.total_spent || 0}
              </p>
            </div>
            <div className="bg-amber-50 rounded-xl p-4 text-center">
              <p className="text-sm text-amber-800">
                با هر ۱۰ امتیاز، ۱,۰۰۰ تومان تخفیف در کیف پول شما شارژ می‌شود.
              </p>
            </div>
          </div>
        )}

        {activeTab === "transactions" && (
          <div>
            {transactions.length === 0 ? (
              <div className="card text-center py-8 text-gray-400">تراکنشی یافت نشد.</div>
            ) : (
              <div className="space-y-3">
                {transactions.map((t) => (
                  <div key={t.id} className="card flex justify-between items-center">
                    <div>
                      <p className="font-medium">{t.type_display || t.transaction_type}</p>
                      <p className="text-sm text-gray-500">{t.created_at}</p>
                    </div>
                    <span className={`font-bold ${t.status === "success" ? "text-green-600" : "text-yellow-600"}`}>
                      {formatPrice(t.amount)} ت
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
}
