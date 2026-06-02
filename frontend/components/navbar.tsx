"use client";

import { useState } from "react";
import Link from "next/link";
import { useAuth } from "@/lib/auth-context";
import {
  Scissors,
  Menu,
  X,
  User,
  LogOut,
  Calendar,
  ShoppingBag,
  Heart,
} from "lucide-react";

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);

  const navLinks = [
    { href: "/services", label: "خدمات" },
    { href: "/booking", label: "رزرو نوبت" },
    { href: "/gallery", label: "گالری" },
    { href: "/products", label: "محصولات" },
    { href: "/contact", label: "تماس" },
  ];

  return (
    <nav className="sticky top-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex items-center gap-2">
              <div className="w-9 h-9 rounded-lg bg-rose-600 flex items-center justify-center">
                <Scissors className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">فائزه</span>
            </Link>
          </div>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="px-3 py-2 text-sm text-gray-600 hover:text-rose-600 rounded-lg hover:bg-rose-50 transition-colors"
              >
                {link.label}
              </Link>
            ))}
          </div>

          <div className="hidden md:flex items-center gap-3">
            {isAuthenticated ? (
              <div className="flex items-center gap-3">
                <Link
                  href="/dashboard"
                  className="flex items-center gap-2 px-3 py-2 text-sm text-gray-600 hover:text-rose-600 rounded-lg hover:bg-rose-50 transition-colors"
                >
                  <User className="w-4 h-4" />
                  {user?.first_name || "پروفایل"}
                </Link>
                <button
                  onClick={logout}
                  className="flex items-center gap-1 px-3 py-2 text-sm text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link href="/login" className="btn-secondary text-sm py-2">
                  ورود
                </Link>
                <Link href="/register" className="btn-primary text-sm py-2">
                  ثبت‌نام
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="p-2 text-gray-600 hover:text-rose-600"
            >
              {menuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {menuOpen && (
        <div className="md:hidden bg-white border-t border-gray-100">
          <div className="px-4 py-3 space-y-1">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMenuOpen(false)}
                className="block px-3 py-2 text-gray-600 hover:text-rose-600 hover:bg-rose-50 rounded-lg"
              >
                {link.label}
              </Link>
            ))}
            {isAuthenticated ? (
              <>
                <Link
                  href="/dashboard"
                  onClick={() => setMenuOpen(false)}
                  className="flex items-center gap-2 px-3 py-2 text-gray-600 hover:text-rose-600 hover:bg-rose-50 rounded-lg"
                >
                  <User className="w-4 h-4" />
                  پروفایل
                </Link>
                <button
                  onClick={() => {
                    setMenuOpen(false);
                    logout();
                  }}
                  className="flex items-center gap-2 w-full px-3 py-2 text-red-500 hover:bg-red-50 rounded-lg"
                >
                  <LogOut className="w-4 h-4" />
                  خروج
                </button>
              </>
            ) : (
              <div className="flex gap-2 pt-2 border-t border-gray-100">
                <Link href="/login" onClick={() => setMenuOpen(false)} className="flex-1 btn-secondary text-center text-sm py-2">
                  ورود
                </Link>
                <Link href="/register" onClick={() => setMenuOpen(false)} className="flex-1 btn-primary text-center text-sm py-2">
                  ثبت‌نام
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}
