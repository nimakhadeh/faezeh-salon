"use client";

import Link from "next/link";
import { Scissors, Phone, MapPin, Instagram, Mail } from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded-lg bg-rose-600 flex items-center justify-center">
                <Scissors className="w-4 h-4 text-white" />
              </div>
              <span className="text-lg font-bold text-white">سالن فائزه</span>
            </div>
            <p className="text-sm leading-relaxed">
              ۴ سال سابقه حرفه‌ای در بافت و اکستنشن مو. هدف ما این است که هر
              مشتری با حس اعتماد به نفس و زیبایی واقعی از سالن خارج بشه.
            </p>
          </div>

          <div>
            <h4 className="text-white font-bold mb-4">لینک‌های سریع</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/services" className="hover:text-rose-400 transition-colors">خدمات</Link></li>
              <li><Link href="/booking" className="hover:text-rose-400 transition-colors">رزرو نوبت</Link></li>
              <li><Link href="/gallery" className="hover:text-rose-400 transition-colors">گالری</Link></li>
              <li><Link href="/products" className="hover:text-rose-400 transition-colors">محصولات</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="text-white font-bold mb-4">خدمات</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/services?type=african" className="hover:text-rose-400 transition-colors">بافت آفریقایی</Link></li>
              <li><Link href="/services?type=brazilian" className="hover:text-rose-400 transition-colors">بافت برزیلی</Link></li>
              <li><Link href="/services?type=extension" className="hover:text-rose-400 transition-colors">اکستنشن مو</Link></li>
              <li><Link href="/services?type=training" className="hover:text-rose-400 transition-colors">آموزش</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="text-white font-bold mb-4">تماس با ما</h4>
            <ul className="space-y-3 text-sm">
              <li className="flex items-center gap-2">
                <Phone className="w-4 h-4 text-rose-500" />
                <span dir="ltr">۰۹۳۹۹۵۴۵۱۱۳</span>
              </li>
              <li className="flex items-center gap-2">
                <MapPin className="w-4 h-4 text-rose-500" />
                ستارخان کوچه ۱۲/۱
              </li>
              <li className="flex items-center gap-2">
                <MapPin className="w-4 h-4 text-rose-500" />
                عفیف‌آباد کوچه ۲۲
              </li>
              <li className="flex items-center gap-2">
                <Instagram className="w-4 h-4 text-rose-500" />
                @Baftmofaezeh
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-10 pt-6 text-center text-sm">
          <p>© ۲۰۲۴ سالن فائزه - تمام حقوق محفوظ است.</p>
          <p className="mt-1 text-gray-500">ظ\u0631\u0641\u062a\u060c \u062f\u0648\u0627\u0645 \u0628\u0627\u0644\u0627\u060c \u062d\u0627\u0644 \u062e\u0648\u0628\u060c \u0627\u0639\u062a\u0645\u0627\u062f \u0628\u0647 \u0646\u0641\u0633</p>
        </div>
      </div>
    </footer>
  );
}
