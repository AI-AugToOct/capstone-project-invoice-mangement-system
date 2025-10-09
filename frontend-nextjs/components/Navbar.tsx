"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { FileText, BarChart3, MessageSquare, Upload, Home, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";
import ThemeToggle from "./ThemeToggle";
import { motion } from "framer-motion";

export default function Navbar() {
  const pathname = usePathname();

  const links = [
    { href: "/", label: "الرئيسية", icon: Home },
    { href: "/upload", label: "رفع فاتورة", icon: Upload },
    { href: "/invoices", label: "الفواتير", icon: FileText },
    { href: "/dashboard", label: "لوحة التحكم", icon: BarChart3 },
    { href: "/chat", label: "الدردشة", icon: MessageSquare },
  ];

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-gray-200/50 dark:border-gray-800/50 bg-white/95 dark:bg-gray-950/95 backdrop-blur-xl shadow-sm">
      <div className="container mx-auto flex h-16 sm:h-18 md:h-20 items-center px-3 sm:px-4 md:px-6 max-w-7xl">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 sm:gap-3 md:gap-4 ml-2 sm:ml-4 md:ml-6 flex-shrink-0">
          <motion.div
            whileHover={{ scale: 1.05 }}
            transition={{ duration: 0.2 }}
          >
            <h1 
              className="text-2xl sm:text-3xl md:text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-[#8dbcc7] to-[#d4a574]"
              style={{ 
                fontFamily: 'var(--font-cairo), Cairo, sans-serif',
                lineHeight: '1.2',
                whiteSpace: 'nowrap'
              }}
            >
              مُـــفـــــوْتِـــــر
            </h1>
          </motion.div>
        </Link>

        {/* Links */}
        <div className="flex items-center gap-1 sm:gap-1.5 md:gap-2 mr-auto">
          {links.map((link) => {
            const Icon = link.icon;
            const isActive = pathname === link.href;
            
            return (
              <Link
                key={link.href}
                href={link.href}
              >
                <motion.div
                  className={cn(
                    "flex items-center gap-1.5 sm:gap-2 md:gap-2.5 px-2 sm:px-3 md:px-5 py-2 sm:py-2.5 md:py-3 rounded-lg sm:rounded-xl text-sm sm:text-base font-semibold transition-all relative overflow-hidden",
                    isActive
                      ? "bg-gradient-to-r from-[#8dbcc7] to-[#d4a574] text-white shadow-md"
                      : "text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800/50"
                  )}
                  whileHover={{ scale: 1.03 }}
                  whileTap={{ scale: 0.98 }}
                >
                  {isActive && (
                    <motion.div
                      layoutId="navbar-indicator"
                      className="absolute inset-0 bg-gradient-to-r from-[#8dbcc7] to-[#d4a574] rounded-lg sm:rounded-xl"
                      transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                    />
                  )}
                  <Icon className={cn("w-4 h-4 sm:w-5 sm:h-5 relative z-10 flex-shrink-0", isActive && "text-white")} />
                  <span className={cn("hidden sm:inline relative z-10 font-bold text-sm md:text-base", isActive && "text-white")}>
                    {link.label}
                  </span>
                </motion.div>
              </Link>
            );
          })}
          
          {/* Theme Toggle */}
          <div className="mr-1 sm:mr-2 md:mr-3">
            <ThemeToggle />
          </div>
        </div>
      </div>
    </nav>
  );
}
