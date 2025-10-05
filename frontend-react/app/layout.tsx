import "./globals.css";
import Link from "next/link";

export const metadata = {
  title: "📊 مفوتر",
  description: "نظام إدارة الفواتير وتحليلها بالذكاء الاصطناعي",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ar" dir="rtl">
      <body className="min-h-screen bg-gradient-to-br from-green-50 to-white text-gray-800 font-tajawal">
        {/* 🔹 Navbar */}
        <nav className="bg-green-600 text-white px-6 py-4 shadow-md flex justify-between items-center">
          <h1 className="text-2xl font-bold">📊 مفوتر</h1>
          <div className="flex gap-6 text-lg">
            <Link href="/" className="hover:text-green-200">🏠 الرئيسية</Link>
            <Link href="/invoices" className="hover:text-green-200">🧾 الفواتير</Link>
            <Link href="/ai" className="hover:text-green-200">🤖 الذكاء الاصطناعي</Link>
            <Link href="/dashboard" className="hover:text-green-200">📈 لوحة التحكم</Link>
          </div>
        </nav>

        {/* 🔹 Page Content */}
        <main className="container mx-auto px-6 py-10">{children}</main>

        {/* 🔹 Footer */}
        <footer className="bg-gray-100 text-center text-gray-600 py-4 border-t mt-10">
          © 2025 <span className="text-green-600 font-bold">مفوتر</span> | جميع الحقوق محفوظة
        </footer>
      </body>
    </html>
  );
}
