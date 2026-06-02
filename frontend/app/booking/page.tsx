"use client";

import { Suspense } from "react";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { servicesApi, appointmentsApi } from "@/lib/api";
import Navbar from "@/components/navbar";
import Footer from "@/components/footer";
import {
  Calendar, Clock, ArrowLeft, Check, User, Scissors,
} from "lucide-react";
import { formatPrice } from "@/lib/utils";
import { motion } from "framer-motion";
import toast, { Toaster } from "react-hot-toast";

const DAYS = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"];

function generateCalendarDays(year: number, month: number) {
  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const days = [];
  // تبدیل یکشنبه (0) به شنبه (6) و ... (برای شروع از شنبه)
  let offset = (firstDay === 0) ? 6 : firstDay - 1;
  for (let i = 0; i < offset; i++) days.push(null);
  for (let d = 1; d <= daysInMonth; d++) days.push(d);
  return days;
}

// ============================================================
// کامپوننت داخلی که تمام logic و useSearchParams را شامل می‌شود
// ============================================================
function BookingContent() {
  const searchParams = useSearchParams();
  const preSelectedService = searchParams.get("service");

  const [step, setStep] = useState(1);
  const [services, setServices] = useState<any[]>([]);
  const [specialists, setSpecialists] = useState<any[]>([]);
  const [selectedService, setSelectedService] = useState<any>(null);
  const [selectedSpecialist, setSelectedSpecialist] = useState<any>(null);
  const [selectedDate, setSelectedDate] = useState("");
  const [selectedTime, setSelectedTime] = useState("");
  const [slots, setSlots] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const today = new Date();
  const [calYear, setCalYear] = useState(today.getFullYear());
  const [calMonth, setCalMonth] = useState(today.getMonth());
  const calendarDays = generateCalendarDays(calYear, calMonth);
  const monthName = new Date(calYear, calMonth).toLocaleString("fa-IR", { month: "long", year: "numeric" });

  useEffect(() => {
    fetchServices();
  }, []);

  useEffect(() => {
    if (selectedService && selectedSpecialist && selectedDate) {
      fetchSlots();
    }
  }, [selectedService, selectedSpecialist, selectedDate]);

  const fetchServices = async () => {
    try {
      const res = await servicesApi.services();
      const svcs = res.data.results || res.data;
      setServices(svcs);
      if (preSelectedService) {
        const pre = svcs.find((s: any) => s.id === Number(preSelectedService));
        if (pre) {
          setSelectedService(pre);
          setStep(2);
        }
      }
      // در صورت وجود API واقعی، متخصصان را از آن دریافت کنید
      // فعلاً mock
      setSpecialists([
        { id: 1, full_name: "فائزه", bio: "۴ سال سابقه" },
        { id: 2, full_name: "مریم", bio: "۶ سال سابقه" },
      ]);
    } catch {
      toast.error("خطا در بارگذاری");
    }
  };

  const fetchSlots = async () => {
    setLoading(true);
    try {
      const res = await appointmentsApi.slots({
        specialist: selectedSpecialist.id,
        service: selectedService.id,
        date: selectedDate,
      });
      setSlots(res.data.slots || []);
    } catch {
      toast.error("خطا در دریافت زمان‌ها");
    } finally {
      setLoading(false);
    }
  };

  const handleBook = async () => {
    if (!selectedService || !selectedSpecialist || !selectedDate || !selectedTime) {
      toast.error("لطفاً همه موارد را انتخاب کنید.");
      return;
    }
    setLoading(true);
    try {
      const [hour, minute] = selectedTime.split(":");
      const endHour = String(Number(hour) + 1).padStart(2, "0");
      const res = await appointmentsApi.create({
        specialist: selectedSpecialist.id,
        service: selectedService.id,
        date: selectedDate,
        start_time: selectedTime,
        end_time: `${endHour}:${minute}`,
      });
      toast.success("نوبت با موفقیت ثبت شد!");
      if (res.data.payment_url) {
        window.location.href = res.data.payment_url;
      } else {
        setStep(5);
      }
    } catch (err: any) {
      toast.error(err.response?.data?.error || "خطا در ثبت نوبت");
    } finally {
      setLoading(false);
    }
  };

  const selectDate = (day: number) => {
    const date = `${calYear}-${String(calMonth + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
    setSelectedDate(date);
  };

  return (
    <>
      <Navbar />

      <div className="bg-gradient-to-br from-rose-50 to-pink-50 py-10">
        <div className="max-w-4xl mx-auto px-4">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">رزرو نوبت</h1>
          <p className="text-gray-600">چند مرحله ساده تا رزرو نوبت شما</p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Steps */}
        <div className="flex items-center justify-between mb-8">
          {[
            { num: 1, label: "انتخاب خدمت" },
            { num: 2, label: "انتخاب متخصص" },
            { num: 3, label: "تاریخ و زمان" },
            { num: 4, label: "تأیید" },
          ].map((s) => (
            <div key={s.num} className="flex items-center gap-2">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                step >= s.num ? "bg-rose-600 text-white" : "bg-gray-200 text-gray-500"
              }`}>
                {step > s.num ? <Check className="w-4 h-4" /> : s.num}
              </div>
              <span className={`hidden sm:block text-sm ${step >= s.num ? "text-rose-600 font-medium" : "text-gray-400"}`}>
                {s.label}
              </span>
            </div>
          ))}
        </div>

        {/* Step 1: Select Service */}
        {step === 1 && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <h2 className="text-xl font-bold text-gray-900 mb-4">انتخاب خدمت</h2>
            <div className="grid sm:grid-cols-2 gap-4">
              {services.map((s) => (
                <button
                  key={s.id}
                  onClick={() => { setSelectedService(s); setStep(2); }}
                  className={`bg-white p-4 rounded-xl shadow-sm border text-right hover:shadow-md transition-all ${
                    selectedService?.id === s.id ? "ring-2 ring-rose-500" : ""
                  }`}
                >
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-xl bg-rose-100 flex items-center justify-center flex-shrink-0">
                      <Scissors className="w-6 h-6 text-rose-600" />
                    </div>
                    <div>
                      <h3 className="font-bold text-gray-900">{s.name}</h3>
                      <p className="text-sm text-gray-500 line-clamp-1">{s.description}</p>
                      <div className="flex items-center gap-4 mt-2">
                        <span className="text-rose-600 font-bold text-sm">{formatPrice(s.base_price)} تومان</span>
                        <span className="text-xs text-gray-400 flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          {s.duration_minutes} دقیقه
                        </span>
                      </div>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </motion.div>
        )}

        {/* Step 2: Select Specialist */}
        {step === 2 && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <h2 className="text-xl font-bold text-gray-900 mb-4">انتخاب متخصص</h2>
            <div className="grid sm:grid-cols-2 gap-4">
              {specialists.map((sp) => (
                <button
                  key={sp.id}
                  onClick={() => { setSelectedSpecialist(sp); setStep(3); }}
                  className={`bg-white p-4 rounded-xl shadow-sm border text-right hover:shadow-md transition-all ${
                    selectedSpecialist?.id === sp.id ? "ring-2 ring-rose-500" : ""
                  }`}
                >
                  <div className="flex items-center gap-4">
                    <div className="w-14 h-14 rounded-full bg-rose-200 flex items-center justify-center">
                      <User className="w-7 h-7 text-rose-700" />
                    </div>
                    <div>
                      <h3 className="font-bold text-gray-900">{sp.full_name}</h3>
                      <p className="text-sm text-gray-500">{sp.bio}</p>
                    </div>
                  </div>
                </button>
              ))}
            </div>
            <button onClick={() => setStep(1)} className="mt-4 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              <ArrowLeft className="w-4 h-4 inline ml-2" />
              مرحله قبل
            </button>
          </motion.div>
        )}

        {/* Step 3: Select Date & Time */}
        {step === 3 && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <h2 className="text-xl font-bold text-gray-900 mb-4">انتخاب تاریخ</h2>
            <div className="bg-white p-4 rounded-xl shadow-sm border mb-6">
              <div className="flex justify-between items-center mb-4">
                <button onClick={() => setCalMonth((m) => (m === 0 ? 11 : m - 1))} className="p-2 hover:bg-gray-100 rounded-lg">
                  <ArrowLeft className="w-5 h-5" />
                </button>
                <span className="font-bold">{monthName}</span>
                <button onClick={() => setCalMonth((m) => (m === 11 ? 0 : m + 1))} className="p-2 hover:bg-gray-100 rounded-lg">
                  <ArrowLeft className="w-5 h-5 rotate-180" />
                </button>
              </div>
              <div className="grid grid-cols-7 gap-1 text-center mb-2">
                {DAYS.map((d) => (
                  <div key={d} className="text-xs font-medium text-gray-500 py-2">{d}</div>
                ))}
              </div>
              <div className="grid grid-cols-7 gap-1">
                {calendarDays.map((day, i) => (
                  <button
                    key={i}
                    disabled={!day}
                    onClick={() => day && selectDate(day)}
                    className={`py-2 rounded-lg text-sm transition-colors ${
                      !day
                        ? "invisible"
                        : selectedDate === `${calYear}-${String(calMonth + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`
                        ? "bg-rose-600 text-white"
                        : "hover:bg-rose-50 text-gray-700"
                    }`}
                  >
                    {day}
                  </button>
                ))}
              </div>
            </div>

            {selectedDate && (
              <>
                <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <Clock className="w-5 h-5 text-rose-600" />
                  انتخاب زمان
                </h3>
                {loading ? (
                  <div className="text-center py-8 text-gray-400">در حال بارگذاری...</div>
                ) : (
                  <div className="grid grid-cols-3 sm:grid-cols-4 gap-3 mb-6">
                    {slots.map((slot: any, i: number) => (
                      <button
                        key={i}
                        disabled={!slot.is_available}
                        onClick={() => setSelectedTime(slot.start_time)}
                        className={`py-2.5 rounded-lg text-sm font-medium transition-colors ${
                          selectedTime === slot.start_time
                            ? "bg-rose-600 text-white"
                            : slot.is_available
                            ? "bg-white border border-gray-200 hover:border-rose-300 text-gray-700"
                            : "bg-gray-100 text-gray-400 cursor-not-allowed line-through"
                        }`}
                      >
                        {slot.start_time}
                      </button>
                    ))}
                  </div>
                )}
              </>
            )}

            <div className="flex gap-3">
              <button
                onClick={() => selectedTime ? setStep(4) : toast.error("زمان را انتخاب کنید.")}
                className="px-6 py-2 bg-rose-600 text-white rounded-lg hover:bg-rose-700"
              >
                ادامه
              </button>
              <button onClick={() => setStep(2)} className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                <ArrowLeft className="w-4 h-4 inline ml-2" />
                مرحله قبل
              </button>
            </div>
          </motion.div>
        )}

        {/* Step 4: Confirm */}
        {step === 4 && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <h2 className="text-xl font-bold text-gray-900 mb-4">تأیید نوبت</h2>
            <div className="bg-white p-5 rounded-xl shadow-sm border space-y-4">
              <div className="flex justify-between py-3 border-b border-gray-100">
                <span className="text-gray-500">خدمت</span>
                <span className="font-medium">{selectedService?.name}</span>
              </div>
              <div className="flex justify-between py-3 border-b border-gray-100">
                <span className="text-gray-500">متخصص</span>
                <span className="font-medium">{selectedSpecialist?.full_name}</span>
              </div>
              <div className="flex justify-between py-3 border-b border-gray-100">
                <span className="text-gray-500">تاریخ</span>
                <span className="font-medium">{selectedDate}</span>
              </div>
              <div className="flex justify-between py-3 border-b border-gray-100">
                <span className="text-gray-500">ساعت</span>
                <span className="font-medium">{selectedTime}</span>
              </div>
              <div className="flex justify-between py-3 border-b border-gray-100">
                <span className="text-gray-500">قیمت کل</span>
                <span className="font-medium">{formatPrice(selectedService?.base_price || 0)} تومان</span>
              </div>
              {selectedService?.requires_deposit && (
                <div className="flex justify-between py-3 bg-amber-50 rounded-lg px-4">
                  <span className="text-amber-700">بیعانه ({selectedService?.deposit_percent}٪)</span>
                  <span className="font-bold text-amber-700">
                    {formatPrice(Math.floor((selectedService?.base_price || 0) * (selectedService?.deposit_percent || 30) / 100))} تومان
                  </span>
                </div>
              )}
            </div>

            <div className="flex gap-3 mt-6">
              <button onClick={handleBook} disabled={loading} className="px-6 py-2 bg-rose-600 text-white rounded-lg hover:bg-rose-700 disabled:opacity-50">
                {loading ? "در حال ثبت..." : "ثبت نوبت و پرداخت"}
              </button>
              <button onClick={() => setStep(3)} className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                <ArrowLeft className="w-4 h-4 inline ml-2" />
                ویرایش
              </button>
            </div>
          </motion.div>
        )}

        {/* Step 5: Success */}
        {step === 5 && (
          <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="text-center py-16">
            <div className="w-20 h-20 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-6">
              <Check className="w-10 h-10 text-green-600" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">نوبت با موفقیت ثبت شد!</h2>
            <p className="text-gray-600 mb-8">پیامک تأیید برای شما ارسال شد.</p>
            <div className="flex gap-4 justify-center">
              <Link href="/dashboard" className="px-6 py-2 bg-rose-600 text-white rounded-lg hover:bg-rose-700">
                مشاهده نوبت‌ها
              </Link>
              <Link href="/" className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                صفحه اصلی
              </Link>
            </div>
          </motion.div>
        )}
      </div>

      <Footer />
    </>
  );
}

// ============================================================
// کامپوننت اصلی با Suspense (رفع خطای useSearchParams در build)
// ============================================================
export default function BookingPage() {
  return (
    <>
      <Toaster position="top-center" />
      <Suspense fallback={
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="w-12 h-12 border-4 border-rose-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-gray-500">در حال بارگذاری...</p>
          </div>
        </div>
      }>
        <BookingContent />
      </Suspense>
    </>
  );
}
