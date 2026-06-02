"use client";

import { useEffect, useState } from "react";
import { servicesApi } from "@/lib/api";
import Navbar from "@/components/navbar";
import Footer from "@/components/footer";
import { ShoppingBag, Tag } from "lucide-react";
import { formatPrice } from "@/lib/utils";
import toast, { Toaster } from "react-hot-toast";

export default function ProductsPage() {
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await servicesApi.products();
        setProducts(res.data.results || res.data);
      } catch {
        toast.error("خطا در بارگذاری محصولات");
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
          <h1 className="text-3xl font-bold text-gray-900 mb-2">محصولات</h1>
          <p className="text-gray-600">محصولات مراقبت از مو و بافت</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {loading ? (
          <div className="text-center py-20 text-gray-400">در حال بارگذاری...</div>
        ) : products.length === 0 ? (
          <div className="text-center py-20">
            <ShoppingBag className="w-16 h-16 mx-auto mb-4 text-gray-300" />
            <p className="text-gray-500">محصولی موجود نیست.</p>
          </div>
        ) : (
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {products.map((p: any) => (
              <div key={p.id} className="card hover:shadow-lg transition-shadow">
                <div className="aspect-square bg-rose-50 rounded-lg mb-4 flex items-center justify-center">
                  <ShoppingBag className="w-10 h-10 text-rose-300" />
                </div>
                <h3 className="font-bold text-gray-900 mb-1">{p.name}</h3>
                <p className="text-sm text-gray-500 mb-3 line-clamp-2">{p.description}</p>
                <div className="flex items-center justify-between">
                  <div>
                    {p.has_discount ? (
                      <>
                        <span className="text-rose-600 font-bold">{formatPrice(p.final_price)} ت</span>
                        <span className="text-sm text-gray-400 line-through mr-2">{formatPrice(p.price)}</span>
                      </>
                    ) : (
                      <span className="text-rose-600 font-bold">{formatPrice(p.price)} ت</span>
                    )}
                  </div>
                  {p.has_discount && (
                    <span className="text-xs bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full flex items-center gap-1">
                      <Tag className="w-3 h-3" />
                      {p.discount_percent}٪
                    </span>
                  )}
                </div>
                {!p.is_in_stock && (
                  <p className="text-xs text-red-500 mt-2">ناموجود</p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
}
