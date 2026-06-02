"use client";

import { useEffect, useState } from "react";
import { galleryApi } from "@/lib/api";
import Navbar from "@/components/navbar";
import Footer from "@/components/footer";
import { Sparkles } from "lucide-react";
import toast, { Toaster } from "react-hot-toast";

export default function GalleryPage() {
  const [images, setImages] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await galleryApi.public();
        setImages(res.data.results || res.data);
      } catch {
        toast.error("خطا در بارگذاری گالری");
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

      <div className="bg-gradient-to-br from-rose-50 to-pink-50 py-12">
        <div className="max-w-7xl mx-auto px-4">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">گالری نمونه کارها</h1>
          <p className="text-gray-600">Before / After</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {loading ? (
          <div className="text-center py-20 text-gray-400">در حال بارگذاری...</div>
        ) : images.length === 0 ? (
          <div className="text-center py-20">
            <Sparkles className="w-16 h-16 mx-auto mb-4 text-gray-300" />
            <p className="text-gray-500">نمونه کارها به زودی اضافه می‌شوند.</p>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {images.map((img: any) => (
              <div key={img.id} className="card">
                <div className="grid grid-cols-2 gap-2 mb-4">
                  <div className="aspect-square bg-rose-50 rounded-lg flex items-center justify-center">
                    <span className="text-sm text-gray-400">Before</span>
                  </div>
                  <div className="aspect-square bg-rose-100 rounded-lg flex items-center justify-center">
                    <span className="text-sm text-rose-600 font-medium">After</span>
                  </div>
                </div>
                <h3 className="font-bold text-gray-900">{img.specialist_name}</h3>
                <p className="text-sm text-gray-500">{img.service_name}</p>
                {img.description && <p className="text-sm text-gray-600 mt-2">{img.description}</p>}
              </div>
            ))}
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
}
