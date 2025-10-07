import type { Metadata } from "next";
import { Cairo } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";
import { Toaster } from "@/components/ui/toaster";
import { ThemeProvider } from "@/components/theme-provider";

const cairo = Cairo({
  subsets: ["arabic"],
  weight: ["400", "600", "700"],
  variable: "--font-cairo",
});

export const metadata: Metadata = {
  title: "مُـفـــــوْتِــــر - نظام ذكي لإدارة الفواتير",
  description: "يحفظ، يدير، يحلل، ويختصر وقتك",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ar" dir="rtl" className={cairo.variable} suppressHydrationWarning>
      <body className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-green-50 dark:from-gray-900 dark:via-blue-950 dark:to-green-950">
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <Navbar />
          {children}
          <footer className="py-6 text-center text-sm text-muted-foreground border-t">
            <p>© 2025 مُـفـــــوْتِــــر - جميع الحقوق محفوظة</p>
            <p className="text-xs mt-1 text-muted-foreground/70">يحفظ، يدير، يحلل، ويختصر وقتك</p>
          </footer>
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  );
}

