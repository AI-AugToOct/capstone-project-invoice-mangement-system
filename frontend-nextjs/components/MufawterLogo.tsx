"use client";

import { motion } from "framer-motion";

interface MufawterLogoProps {
  size?: "sm" | "md" | "lg" | "xl";
  className?: string;
}

export default function MufawterLogo({ 
  size = "lg", 
  className = ""
}: MufawterLogoProps) {
  
  const sizeMap = {
    sm: "text-3xl sm:text-4xl",
    md: "text-4xl sm:text-5xl md:text-6xl",
    lg: "text-5xl sm:text-6xl md:text-7xl",
    xl: "text-6xl sm:text-7xl md:text-8xl"
  };
  
  const textSize = sizeMap[size];

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className={`flex justify-center ${className}`}
    >
      <h1 
        className={`${textSize} font-black text-transparent bg-clip-text bg-gradient-to-r from-[#8dbcc7] to-[#d4a574]`}
        style={{ 
          fontFamily: 'var(--font-cairo), Cairo, sans-serif',
          lineHeight: '1.3',
          filter: 'drop-shadow(0 0 20px rgba(141, 188, 199, 0.3))'
        }}
      >
        مُـــفـــــوْتِـــــر
      </h1>
    </motion.div>
  );
}

