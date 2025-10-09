"use client";

import { motion } from "framer-motion";
import Image from "next/image";

interface MufawterLogoProps {
  size?: "sm" | "md" | "lg" | "xl";
  className?: string;
}

export default function MufawterLogo({ 
  size = "lg", 
  className = ""
}: MufawterLogoProps) {
  
  const sizeMap = {
    sm: { width: 200, height: 60 },
    md: { width: 280, height: 84 },
    lg: { width: 360, height: 108 },
    xl: { width: 400, height: 120 }
  };
  
  const dimensions = sizeMap[size];

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className={`flex justify-center ${className}`}
    >
      <Image
        src="/logo-mufawter.svg"
        alt="مُـــفـــــوْتِــــر"
        width={dimensions.width}
        height={dimensions.height}
        priority
        className="w-auto h-auto max-w-full"
        style={{
          filter: 'drop-shadow(0 0 20px rgba(141, 188, 199, 0.3))'
        }}
      />
    </motion.div>
  );
}

