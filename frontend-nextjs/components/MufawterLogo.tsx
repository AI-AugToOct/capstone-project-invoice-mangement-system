"use client";

import { motion } from "framer-motion";

interface MufawterLogoProps {
  size?: "sm" | "md" | "lg" | "xl";
  showEnglish?: boolean;
  className?: string;
}

export default function MufawterLogo({ 
  size = "lg", 
  showEnglish = false,
  className = ""
}: MufawterLogoProps) {
  
  const sizeClasses = {
    sm: "text-2xl sm:text-3xl",
    md: "text-3xl sm:text-4xl md:text-5xl",
    lg: "text-4xl sm:text-5xl md:text-6xl lg:text-7xl",
    xl: "text-5xl sm:text-6xl md:text-7xl lg:text-8xl"
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className={`text-center ${className}`}
    >
      <h1 
        className={`${sizeClasses[size]} font-black text-transparent bg-clip-text bg-gradient-to-r from-[#8dbcc7] to-[#d4a574] leading-tight tracking-tight`}
        style={{
          fontFamily: 'var(--font-cairo), Cairo, Tajawal, sans-serif',
          textShadow: '0 0 40px rgba(141, 188, 199, 0.2)',
        }}
      >
        مُـفـَـوْتِــر
        {showEnglish && (
          <>
            <span className="text-gray-400 dark:text-gray-600 mx-2 sm:mx-3">|</span>
            <span className="text-gray-700 dark:text-gray-300 text-[0.7em]">
              MuFawter
            </span>
          </>
        )}
      </h1>
    </motion.div>
  );
}

