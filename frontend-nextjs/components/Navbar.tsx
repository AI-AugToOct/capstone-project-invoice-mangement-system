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
    <nav className="sticky top-0 z-50 w-full border-0 bg-white/80 dark:bg-gray-950/80 backdrop-blur-xl shadow-sm">
      <div className="container mx-auto flex h-20 items-center px-4 max-w-7xl">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-3 ml-8">
          <motion.div 
            className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#8dbcc7] to-[#d4a574] flex items-center justify-center shadow-lg"
            whileHover={{ rotate: [0, -10, 10, 0], scale: 1.1 }}
            transition={{ duration: 0.3 }}
          >
            <Sparkles className="w-6 h-6 text-white" />
          </motion.div>
          <div className="flex flex-col">
            <span className="text-2xl font-black bg-gradient-to-r from-[#8dbcc7] to-[#d4a574] bg-clip-text text-transparent">
              مُـفـــــوْتِــــر
            </span>
            <span className="text-[10px] text-muted-foreground -mt-1">
              مدعوم بالذكاء الاصطناعي
            </span>
          </div>
        </Link>

        {/* Links */}
        <div className="flex items-center gap-1 mr-auto">
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
                    "flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold transition-all relative overflow-hidden",
                    isActive
                      ? "bg-gradient-to-r from-[#8dbcc7] to-[#d4a574] text-white shadow-lg shadow-[#8dbcc7]/30"
                      : "text-muted-foreground hover:text-foreground hover:bg-accent/50"
                  )}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  {isActive && (
                    <motion.div
                      layoutId="navbar-indicator"
                      className="absolute inset-0 bg-gradient-to-r from-[#8dbcc7] to-[#d4a574] rounded-xl"
                      transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                    />
                  )}
                  <Icon className={cn("w-4 h-4 relative z-10", isActive && "text-white")} />
                  <span className={cn("hidden sm:inline relative z-10", isActive && "text-white")}>
                    {link.label}
                  </span>
                </motion.div>
              </Link>
            );
          })}
          
          {/* Theme Toggle */}
          <div className="mr-2">
            <ThemeToggle />
          </div>
        </div>
      </div>
    </nav>
  );
}
