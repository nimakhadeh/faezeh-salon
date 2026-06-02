"use client";

import Navbar from "@/components/navbar";
import Footer from "@/components/footer";
import { Phone, MapPin, Instagram, Clock, MessageCircle } from "lucide-react";
import Link from "next/link";

export default function ContactPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="bg-gradient-to-br from-rose-50 to-pink-50 py-12">
        <div className="max-w-7xl mx-auto px-4">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">تماس با ما</h1>
          <p className="text-gray-600">ما اینجاییم تا زیباترین تجربه را برای شما بسازیم</p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="grid md:grid-cols-2 gap-8">
          <div className="space-y-6">
            <div className="card flex items-start gap-4">
              <div className="w-12 h-12 rounded-xl bg-rose-100 flex items-center justify-center flex-shrink-0">
                <Phone className="w-6 h-6 text-rose-600" />
              </div>
              <div>
                <h3 className="font-bold text-gray-900">شماره تماس</h3>
                <p className="text-gray-600 mt-1" dir="ltr">۰۹۳۹۹۵۴۵۱۱۳</p>
                <p className="text-sm text-gray-500">فائزه</p>
              </div>
            </div>

            <div className="card flex items-start gap-4">
              <div className="w-12 h-12 rounded-xl bg-rose-100 flex items-center justify-center flex-shrink-0">
                <MapPin className="w-6 h-6 text-rose-600" />
              </div>
              <div>
                <h3 className="font-bold text-gray-900">آدرس</h3>
                <p className="text-gray-600 mt-1">ستارخان کوچه ۱۲/۱</p>
                <p className="text-gray-600">عفیف‌آباد کوچه ۲۲</p>
              </div>
            </div>

            <div className="card flex items-start gap-4">
              <div className="w-12 h-12 rounded-xl bg-rose-100 flex items-center justify-center flex-shrink-0">
                <Instagram className="w-6 h-6 text-rose-600" />
              </div>
              <div>
                <h3 className="font-bold text-gray-900">اینستاگرام</h3>
                <p className="text-gray-600 mt-1">@Baftmofaezeh</p>
                <a href="https://instagram.com/Baftmofaezeh" target="_blank" rel="noopener noreferrer" className="text-rose-600 text-sm mt-1 inline-block">
                  مشاهده پیج
                </a>
              </div>
            </div>

            <div className="card flex items-start gap-4">
              <div className="w-12 h-12 rounded-xl bg-rose-100 flex items-center justify-center flex-shrink-0">
                <Clock className="w-6 h-6 text-rose-600" />
              </div>
              <div>
                <h3 className="font-bold text-gray-900">ساعات کاری</h3>
                <div className="text-gray-600 mt-1 space-y-1 text-sm">
                  <p>شنبه - چهارشنبه: ۱۰ صبح تا ۸ شب</p>
                  <p>پنجشنبه: ۱۰ صبح تا ۶ شب</p>
                  <p>جمعه: تعطیل</p>
                </div>
              </div>
            </div>
          </div>

          <div className="card bg-gradient-to-br from-rose-500 to-pink-600 text-white">
            <h2 className="text-2xl font-bold mb-4">رزرو نوبت</h2>
            <p className="mb-6 leading-relaxed">
              برای رزرو نوبت می‌توانید از طریق سایت اقدام کنید یا با شماره
              ۰۹۳۹۹۵۴۵۱۱۳ تماس بگیرید.
            </p>
            <Link href="/booking" className="block w-full bg-white text-rose-600 text-center py-3 rounded-xl font-bold hover:bg-rose-50 transition-colors">
              رزرو آنلاین نوبت
            </Link>
            <div className="mt-6 pt-6 border-t border-white/20">
              <p className="text-sm opacity-90">
                "ظ\u0631\u0641\u062a\u060c \u062f\u0648\u0627\u0645 \u0628\u0627\u0644\u0627\u060c \u062d\u0627\u0644 \u062e\u0648\u0628\u060c \u0627\u0639\u062a\u0645\u0627\u062f \u0628\u0647 \u0646\u0641\u0633"
              </p>
              <p className="text-sm opacity-75 mt-2">— فائزه</p>
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
}
