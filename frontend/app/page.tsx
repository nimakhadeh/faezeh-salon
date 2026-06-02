"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { useAuth } from "@/lib/auth-context";
import { servicesApi, galleryApi } from "@/lib/api";
import Navbar from "@/components/navbar";
import Footer from "@/components/footer";
import {
  Scissors,
  Heart,
  Shield,
  Sparkles,
  Clock,
  Star,
  ArrowLeft,
  MapPin,
  Phone,
  Instagram,
} from "lucide-react";
import { formatPrice } from "@/lib/utils";
import { motion } from "framer-motion";
import toast, { Toaster } from "react-hot-toast";

const BRAID_TYPES = [
  { key: "african", name: "آفریقایی", color: "bg-purple-500" },
  { key: "brazilian", name: "برزیلی", color: "bg-green-500" },
  { key: "mexican", name: "مکزیکی", color: "bg-red-500" },
  { key: "afro", name: "افرو", color: "bg-yellow-500" },
  { key: "queen", name: "کوئین", color: "bg-pink-500" },
  { key: "dutch", name: "هلندی", color: "bg-orange-500" },
  { key: "french", name: "فرانسوی", color: "bg-blue-500" },
  { key: "combined", name: "ترکیبی", color: "bg-indigo-500" },
];

export default function HomePage() {
  const { user } = useAuth();
  const [services, setServices] = useState<any[]>([]);
  const [gallery, setGallery] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [svRes, galRes] = await Promise.all([
          servicesApi.services(),
          galleryApi.public().catch(() => ({ data: { results: [] } })),
        ]);
        setServices(svRes.data.results?.slice(0, 6) || svRes.data.slice(0, 6));
        setGallery(galRes.data.results?.slice(0, 4) || galRes.data.slice(0, 4));
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <Toaster position="top-center" />
      <Navbar />

      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-rose-50 via-pink-50 to-purple-50 py-20 lg:py-32 overflow-hidden">
        <div className="absolute inset-0 bg-[url('/pattern.png')] opacity-5" />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
            >
              <div className="inline-flex items-center gap-2 bg-rose-100 text-rose-700 px-4 py-1.5 rounded-full text-sm font-medium mb-6">
                <Sparkles className="w-4 h-4" />
                ۴ سال سابقه حرفه‌ای
              </div>
              <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 leading-tight mb-6">
                سالن <span className="text-rose-600">فائزه</span>
                <br />
                بافت و اکستنشن مو
              </h1>
              <p className="text-lg text-gray-600 mb-8 leading-relaxed">
                من فائزه‌ام، ۴ ساله که به‌صورت حرفه‌ای در زمینه بافت و اکستنشن مو
                فعالیت می‌کنم. هدف من این است که هر مشتری با حس اعتماد به نفس و
                زیبایی واقعی از سالن خارج بشه.
              </p>
              <div className="flex flex-wrap gap-4">
                <Link href="/booking" className="btn-primary text-base px-6 py-3">
                  <Scissors className="w-5 h-5 mr-2" />
                  رزرو نوبت
                </Link>
                <Link href="/services" className="btn-secondary text-base px-6 py-3">
                  مشاهده خدمات
                  <ArrowLeft className="w-5 h-5 mr-2" />
                </Link>
              </div>
              <div className="flex gap-8 mt-10">
                <div className="text-center">
                  <div className="text-2xl font-bold text-rose-600">۱۸+</div>
                  <div className="text-sm text-gray-500">نوع بافت</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-rose-600">۴</div>
                  <div className="text-sm text-gray-500">سال سابقه</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-rose-600">۱۰۰۰+</div>
                  <div className="text-sm text-gray-500">مشتری راضی</div>
                </div>
              </div>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="relative"
            >
              <div className="relative rounded-3xl overflow-hidden shadow-2xl bg-rose-100 aspect-[4/5] flex items-center justify-center">
                <Scissors className="w-32 h-32 text-rose-300" />
                <div className="absolute bottom-6 left-6 right-6 bg-white/90 backdrop-blur-sm rounded-2xl p-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-full bg-rose-200 flex items-center justify-center">
                      <Heart className="w-6 h-6 text-rose-600" />
                    </div>
                    <div>
                      <div className="font-semibold text-gray-900">رضایت مشتریان</div>
                      <div className="text-sm text-gray-500">۹۵٪ رضایت</div>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="section-title">چرا سالن فائزه؟</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              کیفیت، دوام بالا، ظرافت و حال خوب - این‌ها چیزی است که ما به هر
              مشتری وعده می‌دهیم.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { icon: Scissors, title: "تنوع بالا", desc: "۱۸+ نوع بافت و اکستنشن" },
              { icon: Shield, title: "دوام بالا", desc: "استفاده از متریال باکیفیت" },
              { icon: Star, title: "ظ\u0631\u0641\u062a", desc: "دقت در جزئیات" },
              { icon: Heart, title: "حال خوب", desc: "تجربه لذت‌بخش" },
            ].map((f, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="card text-center hover:shadow-md transition-shadow"
              >
                <div className="w-14 h-14 rounded-2xl bg-rose-100 flex items-center justify-center mx-auto mb-4">
                  <f.icon className="w-7 h-7 text-rose-600" />
                </div>
                <h3 className="font-bold text-gray-900 mb-2">{f.title}</h3>
                <p className="text-sm text-gray-500">{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Braid Types */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="section-title">انواع بافت</h2>
            <p className="text-gray-600">از بافت‌های ساده تا پیشرفته و ژورنالی</p>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {BRAID_TYPES.map((bt, i) => (
              <Link href={`/services?type=${bt.key}`} key={i}>
                <motion.div
                  initial={{ opacity: 0, scale: 0.9 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  transition={{ delay: i * 0.05 }}
                  className="bg-white rounded-xl p-6 text-center shadow-sm hover:shadow-md transition-all cursor-pointer border border-gray-100"
                >
                  <div className={`w-10 h-10 rounded-lg ${bt.color} mx-auto mb-3`} />
                  <span className="text-sm font-medium text-gray-700">{bt.name}</span>
                </motion.div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Services Preview */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-8">
            <h2 className="section-title mb-0">محبوب‌ترین خدمات</h2>
            <Link href="/services" className="text-rose-600 hover:text-rose-700 text-sm font-medium flex items-center">
              مشاهده همه
              <ArrowLeft className="w-4 h-4 mr-1" />
            </Link>
          </div>
          {loading ? (
            <div className="text-center py-12 text-gray-400">در حال بارگذاری...</div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {services.map((s: any, i: number) => (
                <motion.div
                  key={s.id}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.1 }}
                  className="card hover:shadow-lg transition-shadow"
                >
                  <div className="aspect-video bg-rose-50 rounded-lg mb-4 flex items-center justify-center">
                    <Scissors className="w-10 h-10 text-rose-300" />
                  </div>
                  <h3 className="font-bold text-gray-900 mb-1">{s.name}</h3>
                  <p className="text-sm text-gray-500 mb-3 line-clamp-2">{s.description}</p>
                  <div className="flex justify-between items-center">
                    <span className="text-rose-600 font-bold">{formatPrice(s.base_price)} تومان</span>
                    <span className="text-xs text-gray-400 flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {s.duration_minutes} دقیقه
                    </span>
                  </div>
                  <Link href={`/booking?service=${s.id}`} className="btn-primary w-full mt-4 text-sm">
                    رزرو نوبت
                  </Link>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Gallery Preview */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="section-title">گالری نمونه کارها</h2>
            <p className="text-gray-600">Before / After</p>
          </div>
          {gallery.length > 0 ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
              {gallery.map((g: any, i: number) => (
                <div key={i} className="rounded-xl overflow-hidden shadow-sm">
                  <div className="aspect-square bg-rose-100 flex items-center justify-center">
                    <Sparkles className="w-12 h-12 text-rose-300" />
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12 text-gray-400">
              <Sparkles className="w-16 h-16 mx-auto mb-4 text-gray-300" />
              <p>نمونه کارها به زودی اضافه می‌شوند</p>
            </div>
          )}
          <div className="text-center mt-8">
            <Link href="/gallery" className="btn-primary">
              مشاهده گالری کامل
            </Link>
          </div>
        </div>
      </section>

      {/* Contact */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12">
            <div>
              <h2 className="section-title">تماس با ما</h2>
              <p className="text-gray-600 mb-8">برای رزرو نوبت و مشاوره با ما در تماس باشید.</p>
              <div className="space-y-4">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-xl bg-rose-100 flex items-center justify-center">
                    <Phone className="w-6 h-6 text-rose-600" />
                  </div>
                  <div>
                    <div className="text-sm text-gray-500">شماره تماس</div>
                    <div className="font-semibold text-gray-900" dir="ltr">۰۹۳۹۹۵۴۵۱۱۳</div>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-xl bg-rose-100 flex items-center justify-center">
                    <MapPin className="w-6 h-6 text-rose-600" />
                  </div>
                  <div>
                    <div className="text-sm text-gray-500">آدرس</div>
                    <div className="font-semibold text-gray-900">ستارخان کوچه ۱۲/۱</div>
                    <div className="text-sm text-gray-500">عفیف‌آباد کوچه ۲۲</div>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-xl bg-rose-100 flex items-center justify-center">
                    <Instagram className="w-6 h-6 text-rose-600" />
                  </div>
                  <div>
                    <div className="text-sm text-gray-500">اینستاگرام</div>
                    <div className="font-semibold text-gray-900">@Baftmofaezeh</div>
                  </div>
                </div>
              </div>
            </div>
            <div className="bg-rose-50 rounded-2xl p-8">
              <h3 className="text-xl font-bold text-gray-900 mb-4">ساعات کاری</h3>
              <div className="space-y-3">
                {[
                  { day: "شنبه - چهارشنبه", time: "۱۰ صبح تا ۸ شب" },
                  { day: "پنجشنبه", time: "۱۰ صبح تا ۶ شب" },
                  { day: "جمعه", time: "تعطیل" },
                ].map((s, i) => (
                  <div key={i} className="flex justify-between py-2 border-b border-rose-100">
                    <span className="text-gray-700">{s.day}</span>
                    <span className="font-medium text-gray-900">{s.time}</span>
                  </div>
                ))}
              </div>
              <div className="mt-6 p-4 bg-white rounded-xl">
                <p className="text-sm text-gray-600">
                  "ظ\u0631\u0641\u062a\u060c \u062f\u0648\u0627\u0645 \u0628\u0627\u0644\u0627\u060c \u062d\u0627\u0644 \u062e\u0648\u0628\u060c \u0627\u0639\u062a\u0645\u0627\u062f \u0628\u0647 \u0646\u0641\u0633"
                </p>
                <p className="text-xs text-gray-400 mt-2">— فائزه</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
