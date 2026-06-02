"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { servicesApi } from "@/lib/api";
import Navbar from "@/components/navbar";
import Footer from "@/components/footer";
import {
  Scissors, Clock, ArrowLeft, Filter,
  Search, X,
} from "lucide-react";
import { formatPrice, getBraidTypeLabel, getBraidTypeColor } from "@/lib/utils";
import { motion } from "framer-motion";
import toast, { Toaster } from "react-hot-toast";

const BRAID_TYPES = [
  "african", "brazilian", "mexican", "afro", "queen",
  "dutch", "french", "dreadlock", "combined", "simple",
  "advanced", "minimal", "journal", "daily", "party",
  "travel", "extension_braid", "extension_keratin", "training",
];

export default function ServicesPage() {
  const [services, setServices] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [selectedType, setSelectedType] = useState("");
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    fetchServices();
  }, [selectedType]);

  const fetchServices = async () => {
    setLoading(true);
    try {
      const params: any = {};
      if (selectedType) params.braid_type = selectedType;
      const res = await servicesApi.services(params);
      setServices(res.data.results || res.data);
    } catch {
      toast.error("خطا در بارگذاری خدمات");
    } finally {
      setLoading(false);
    }
  };

  const filtered = services.filter((s) =>
    s.name.includes(search) || s.description.includes(search)
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <Toaster position="top-center" />
      <Navbar />

      <div className="bg-gradient-to-br from-rose-50 to-pink-50 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">خدمات ما</h1>
          <p className="text-gray-600">انواع بافت، اکستنشن و آموزش</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search & Filter */}
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <div className="relative flex-1">
            <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="جستجوی خدمات..."
              className="input-field pr-10"
            />
          </div>
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="btn-secondary flex items-center gap-2"
          >
            <Filter className="w-4 h-4" />
            فیلتر
            {selectedType && <span className="w-2 h-2 rounded-full bg-rose-500" />}
          </button>
        </div>

        {showFilters && (
          <div className="card mb-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-bold text-gray-900">نوع بافت</h3>
              {selectedType && (
                <button onClick={() => setSelectedType("")} className="text-sm text-rose-600 flex items-center gap-1">
                  <X className="w-4 h-4" />
                  پاک کردن
                </button>
              )}
            </div>
            <div className="flex flex-wrap gap-2">
              {BRAID_TYPES.map((t) => (
                <button
                  key={t}
                  onClick={() => setSelectedType(t === selectedType ? "" : t)}
                  className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
                    t === selectedType
                      ? "bg-rose-600 text-white"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}
                >
                  {getBraidTypeLabel(t)}
                </button>
              ))}
            </div>
          </div>
        )}

        {loading ? (
          <div className="text-center py-20 text-gray-400">در حال بارگذاری...</div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-20 text-gray-400">خدمتی یافت نشد.</div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filtered.map((s, i) => (
              <motion.div
                key={s.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className="card hover:shadow-lg transition-shadow"
              >
                <div className="aspect-video bg-rose-50 rounded-lg mb-4 flex items-center justify-center">
                  <Scissors className="w-10 h-10 text-rose-300" />
                </div>
                <div className="flex items-center gap-2 mb-2">
                  <span className={`text-xs px-2 py-0.5 rounded-full ${getBraidTypeColor(s.braid_type)}`}>
                    {getBraidTypeLabel(s.braid_type)}
                  </span>
                  {s.requires_deposit && (
                    <span className="text-xs px-2 py-0.5 rounded-full bg-amber-100 text-amber-700">
                      بیعانه {s.deposit_percent}٪
                    </span>
                  )}
                </div>
                <h3 className="font-bold text-gray-900 mb-1">{s.name}</h3>
                <p className="text-sm text-gray-500 mb-3 line-clamp-2">{s.description}</p>
                <div className="flex justify-between items-center mb-4">
                  <span className="text-rose-600 font-bold">{formatPrice(s.base_price)} تومان</span>
                  <span className="text-xs text-gray-400 flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {s.duration_minutes} دقیقه
                  </span>
                </div>
                <div className="flex gap-2">
                  <Link href={`/booking?service=${s.id}`} className="flex-1 btn-primary text-sm text-center">
                    رزرو نوبت
                  </Link>
                  <Link href={`/services/${s.slug}`} className="btn-secondary text-sm">
                    جزئیات
                    <ArrowLeft className="w-3 h-3 mr-1" />
                  </Link>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
}
