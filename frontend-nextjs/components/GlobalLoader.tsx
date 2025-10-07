"use client";

import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";

interface GlobalLoaderProps {
  message?: string;
  show: boolean;
}

export default function GlobalLoader({ message = "جاري التحميل...", show }: GlobalLoaderProps) {
  if (!show) return null;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-[100] flex items-center justify-center bg-black/50 backdrop-blur-sm"
      dir="rtl"
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="bg-card rounded-2xl shadow-2xl p-8 flex flex-col items-center gap-4 min-w-[300px]"
      >
        <Loader2 className="w-12 h-12 text-primary animate-spin" />
        <p className="text-lg font-semibold text-foreground">{message}</p>
        <div className="w-full h-1 bg-muted rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-blue-500 to-purple-500"
            initial={{ width: "0%" }}
            animate={{ width: ["0%", "100%", "0%"] }}
            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
          />
        </div>
      </motion.div>
    </motion.div>
  );
}

