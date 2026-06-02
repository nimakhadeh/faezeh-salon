import type { Metadata } from "next";
import { AuthProvider } from "@/lib/auth-context";
import "./globals.css";

export const metadata: Metadata = {
  title: "سالن فائزه - بافت و اکستنشن مو",
  description:
    "سالن تخصصی بافت و اکستنشن مو فائزه - ۴ سال سابقه - ظرافت، دوام بالا، حال خوب، اعتماد به نفس",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fa" dir="rtl">
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
