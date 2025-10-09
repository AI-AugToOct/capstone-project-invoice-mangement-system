"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { 
  Upload, 
  BarChart3, 
  MessageSquare, 
  FileText,
  Sparkles,
  Zap,
  Clock,
  Shield,
  TrendingUp,
  ArrowLeft,
  Receipt,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import Image from "next/image";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";
import MufawterLogo from "@/components/MufawterLogo";

export default function Home() {
  const { theme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const features = [
    {
      icon: Upload,
      title: "رفع فوري",
      description: "التقط صورة أو ارفع ملف فاتورتك وسيتم تحليلها خلال ثوان",
      gradient: "from-[#8dbcc7] to-[#6fa3b0]",
      href: "/upload",
    },
    {
      icon: BarChart3,
      title: "تحليل ذكي",
      description: "احصل على رؤى عميقة ورسوم بيانية تفاعلية لمصروفاتك",
      gradient: "from-[#d4a574] to-[#c89563]",
      href: "/dashboard",
    },
    {
      icon: MessageSquare,
      title: "مساعد عربي",
      description: "اسأل المساعد الذكي بالعربية عن أي تفاصيل في فواتيرك",
      gradient: "from-[#8dbcc7] to-[#d4a574]",
      href: "/chat",
    },
    {
      icon: FileText,
      title: "إدارة شاملة",
      description: "عرض وتنظيم وتصدير جميع فواتيرك في مكان واحد",
      gradient: "from-[#d4a574] to-[#8dbcc7]",
      href: "/invoices",
    },
  ];

  const benefits = [
    { icon: Zap, text: "سرعة فائقة" },
    { icon: Clock, text: "يوفر وقتك" },
    { icon: TrendingUp, text: "رؤى دقيقة" },
  ];

  return (
    <div className="relative w-full overflow-hidden">
      
      {/* Hero Section */}
      <section 
        dir="rtl"
        className="relative w-full min-h-screen flex flex-col justify-center items-center text-center px-4 sm:px-6 md:px-16 lg:px-24 xl:px-32 py-16 sm:py-20 md:py-24 overflow-hidden scroll-smooth"
        style={{ scrollSnapAlign: 'start' }}
      >
        {/* Animated Gradient Background */}
        <div className="fixed inset-0 -z-10 animate-gradient opacity-90" />

        <div className="relative z-10 max-w-6xl w-full space-y-6 sm:space-y-8 md:space-y-10">
          
          {/* Main Heading */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="space-y-4 sm:space-y-6"
          >
            {/* Hero Logo */}
            <motion.div
              whileHover={{ scale: 1.05 }}
              transition={{ duration: 0.3 }}
              className="px-4"
            >
              <MufawterLogo size="xl" />
            </motion.div>
            
            <p className="text-lg sm:text-xl md:text-2xl lg:text-3xl text-gray-700 dark:text-gray-300 leading-relaxed max-w-3xl mx-auto px-4">
              نظامك الذكي لرفع، تحليل، وإدارة جميع فواتيرك بضغطة واحدة
            </p>
          </motion.div>

          {/* Benefits Pills */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="flex flex-wrap justify-center gap-2 sm:gap-3 md:gap-4 px-4"
          >
            {benefits.map((benefit, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.3 + index * 0.1 }}
                whileHover={{ scale: 1.05 }}
                className="flex items-center gap-1.5 sm:gap-2 px-3 sm:px-4 md:px-5 py-2 sm:py-2.5 md:py-3 rounded-full bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl shadow-lg border border-[#8dbcc7]/20 text-sm sm:text-base"
              >
                <benefit.icon className="w-4 h-4 sm:w-5 sm:h-5 text-[#8dbcc7] flex-shrink-0" />
                <span className="font-semibold text-gray-800 dark:text-gray-200 whitespace-nowrap">
                  {benefit.text}
                </span>
              </motion.div>
            ))}
          </motion.div>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="flex flex-col sm:flex-row gap-3 sm:gap-4 md:gap-5 justify-center pt-4 sm:pt-6 px-4"
          >
            <Link href="/upload" className="w-full sm:w-auto">
              <Button 
                size="lg"
                className="w-full sm:w-auto group gap-2 sm:gap-3 text-base sm:text-lg md:text-xl px-6 sm:px-10 md:px-12 py-6 sm:py-7 md:py-8 bg-gradient-to-l from-[#8dbcc7] to-[#6fa3b0] hover:from-[#7aabb8] hover:to-[#5f92a0] text-white font-bold shadow-2xl hover:shadow-[#8dbcc7]/50 rounded-xl sm:rounded-2xl transition-all duration-300 hover:scale-105"
              >
                <Upload className="w-5 h-5 sm:w-6 sm:h-6 md:w-7 md:h-7" />
                <span>رفع فاتورة</span>
                <ArrowLeft className="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 group-hover:-translate-x-1 transition-transform" />
              </Button>
            </Link>
            
            <Link href="/dashboard" className="w-full sm:w-auto">
              <Button 
                size="lg"
                variant="outline"
                className="w-full sm:w-auto gap-2 sm:gap-3 text-base sm:text-lg md:text-xl px-6 sm:px-10 md:px-12 py-6 sm:py-7 md:py-8 bg-white/90 dark:bg-gray-900/90 backdrop-blur-xl border-2 border-[#8dbcc7] text-[#8dbcc7] hover:bg-[#8dbcc7]/10 font-bold shadow-xl rounded-xl sm:rounded-2xl transition-all duration-300"
              >
                <BarChart3 className="w-5 h-5 sm:w-6 sm:h-6 md:w-7 md:h-7" />
                <span>شاهد التحليلات</span>
              </Button>
            </Link>
          </motion.div>
          
          {/* Scroll Indicator */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1, duration: 1 }}
            className="absolute bottom-10 left-1/2 -translate-x-1/2"
          >
            <motion.div
              animate={{ y: [0, 10, 0] }}
              transition={{ duration: 1.5, repeat: Infinity }}
              className="flex flex-col items-center gap-2 text-gray-400 dark:text-gray-600 cursor-pointer"
              onClick={() => window.scrollBy({ top: window.innerHeight, behavior: 'smooth' })}
            >
              <span className="text-sm font-medium">اكتشف المزيد</span>
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
              </svg>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* How It Works Section */}
      <section 
        dir="rtl"
        className="relative w-full py-12 sm:py-16 md:py-20 lg:py-24 px-4 sm:px-6 md:px-16 lg:px-24 xl:px-32"
      >
        <div className="max-w-7xl mx-auto">
          
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center space-y-4 sm:space-y-6 md:space-y-8 mb-12 sm:mb-16 md:mb-20 py-2 sm:py-4"
          >
            <h2 
              className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-[#8dbcc7] to-[#d4a574] leading-tight px-4"
              style={{ fontFamily: 'var(--font-cairo), Cairo, sans-serif' }}
            >
              كيف يعمل النظام؟
            </h2>
            <p className="text-sm sm:text-base md:text-lg lg:text-xl text-gray-700 dark:text-gray-300 max-w-3xl mx-auto font-semibold leading-relaxed px-4">
              ثلاث خطوات بسيطة للبدء
            </p>
          </motion.div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 sm:gap-8">
            {[
              {
                step: "1",
                title: "ارفع الفاتورة",
                description: "التقط صورة أو اختر ملف من جهازك",
                icon: Upload,
              },
              {
                step: "2",
                title: "التحليل التلقائي",
                description: "الذكاء الاصطناعي يستخرج كل البيانات",
                icon: Sparkles,
              },
              {
                step: "3",
                title: "شاهد النتائج",
                description: "احصل على رؤى وتحليلات فورية",
                icon: BarChart3,
              },
            ].map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.15 }}
                className="relative group"
              >
                <div className="h-full p-8 rounded-2xl bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-0 shadow-xl hover:shadow-2xl transition-all duration-500">
                  
                  {/* Step Number */}
                  <div className="absolute -top-6 right-8 w-14 h-14 rounded-full bg-gradient-to-br from-[#8dbcc7] to-[#d4a574] flex items-center justify-center text-white text-2xl font-black shadow-lg">
                    {item.step}
                  </div>

                  {/* Icon */}
                  <div className="w-20 h-20 mt-6 mb-6 rounded-2xl bg-gradient-to-br from-[#8dbcc7]/20 to-[#d4a574]/20 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                    <item.icon className="w-10 h-10 text-[#8dbcc7]" />
                  </div>

                  {/* Content */}
                  <h3 className="text-2xl font-black text-gray-900 dark:text-white mb-3">
                    {item.title}
                  </h3>
                  <p className="text-lg text-gray-600 dark:text-gray-400 leading-relaxed">
                    {item.description}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section 
        dir="rtl"
        className="relative w-full py-12 sm:py-16 md:py-20 lg:py-24 px-4 sm:px-6 md:px-16 lg:px-24 xl:px-32 bg-gradient-to-b from-white to-gray-50 dark:from-gray-950 dark:to-gray-900"
      >
        <div className="max-w-7xl mx-auto">
          
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center space-y-3 sm:space-y-4 md:space-y-6 mb-10 sm:mb-12 md:mb-16 py-2 sm:py-4"
          >
            <h2 
              className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-[#8dbcc7] to-[#d4a574] leading-tight px-4"
              style={{ fontFamily: 'var(--font-cairo), Cairo, sans-serif' }}
            >
              مميزات قوية
            </h2>
            <p className="text-sm sm:text-base md:text-lg lg:text-xl text-gray-700 dark:text-gray-300 max-w-3xl mx-auto font-semibold leading-relaxed px-4">
              كل ما تحتاجه لإدارة فواتيرك بذكاء
            </p>
          </motion.div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 md:gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -10 }}
                className="w-full"
              >
                <Link href={feature.href} className="block h-full">
                  <div className="group h-full p-6 sm:p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-lg hover:shadow-2xl border border-gray-100 dark:border-gray-700 transition-all duration-500 cursor-pointer">
                    
                    {/* Icon */}
                    <div className={`w-14 h-14 sm:w-16 sm:h-16 mb-4 sm:mb-6 rounded-2xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center shadow-lg group-hover:scale-110 group-hover:rotate-3 transition-all duration-300`}>
                      <feature.icon className="w-7 h-7 sm:w-8 sm:h-8 text-white" />
                    </div>

                    {/* Content */}
                    <h3 
                      className="text-lg sm:text-xl md:text-2xl font-black text-gray-900 dark:text-white mb-2 sm:mb-3 group-hover:text-[#8dbcc7] transition-colors leading-tight"
                      style={{ fontFamily: 'var(--font-cairo), Cairo, sans-serif' }}
                    >
                      {feature.title}
                    </h3>
                    <p className="text-sm sm:text-base text-gray-600 dark:text-gray-400 leading-relaxed">
                      {feature.description}
                    </p>

                    {/* Arrow */}
                    <div className="flex items-center gap-2 mt-4 sm:mt-6 text-[#8dbcc7] font-bold text-sm opacity-0 group-hover:opacity-100 transition-all">
                      <span>تعرف أكثر</span>
                      <ArrowLeft className="w-4 h-4 sm:w-5 sm:h-5 group-hover:translate-x-1 transition-transform" />
                    </div>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section 
        dir="rtl"
        className="relative w-full py-20 md:py-24 px-6 md:px-16 lg:px-24 xl:px-32 bg-gradient-to-br from-[#8dbcc7] via-[#9fc5cf] to-[#d4a574] overflow-hidden"
      >
        {/* Decorative Elements */}
        <motion.div
          animate={{ rotate: 360, scale: [1, 1.2, 1] }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          className="absolute top-0 left-0 w-96 h-96 bg-white/10 rounded-full blur-3xl"
        />
        <motion.div
          animate={{ rotate: -360, scale: [1, 1.3, 1] }}
          transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
          className="absolute bottom-0 right-0 w-80 h-80 bg-white/10 rounded-full blur-3xl"
        />

        <div className="relative z-10 max-w-4xl mx-auto text-center space-y-10">
          
          {/* Icon */}
          <motion.div
            initial={{ opacity: 0, scale: 0.5 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            animate={{ 
              rotate: [0, 10, -10, 0],
              y: [0, -15, 0]
            }}
            transition={{ 
              rotate: { duration: 4, repeat: Infinity, ease: "easeInOut" },
              y: { duration: 3, repeat: Infinity, ease: "easeInOut" }
            }}
            className="inline-block"
          >
            <div className="w-32 h-32 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center shadow-2xl">
              <Receipt className="w-16 h-16 text-white" />
            </div>
          </motion.div>

          {/* Content */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="space-y-6 sm:space-y-8"
          >
            <h2 
              className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-black text-white leading-tight px-4"
              style={{ fontFamily: 'var(--font-cairo), Cairo, sans-serif' }}
            >
              جاهز لتنظيم فواتيرك؟
            </h2>
            <p className="text-sm sm:text-base md:text-lg lg:text-xl text-white/95 leading-relaxed max-w-2xl mx-auto font-semibold px-4">
              ابدأ الآن واستمتع بتجربة سهلة وسريعة
            </p>
          </motion.div>

          {/* CTA */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="px-4"
          >
            <Link href="/upload" className="inline-block w-full sm:w-auto">
              <Button 
                size="lg"
                className="w-full sm:w-auto gap-2 sm:gap-3 bg-white text-[#8dbcc7] hover:bg-gray-100 font-black text-lg sm:text-xl md:text-2xl px-8 sm:px-12 md:px-14 py-6 sm:py-8 md:py-9 rounded-xl sm:rounded-2xl shadow-2xl hover:scale-105 transition-all"
              >
                <Upload className="w-6 h-6 sm:w-7 sm:h-7 md:w-8 md:h-8" />
                <span>ارفع فاتورة الآن</span>
                <ArrowLeft className="w-5 h-5 sm:w-6 sm:h-6 md:w-7 md:h-7" />
              </Button>
            </Link>
          </motion.div>
        </div>
      </section>

    </div>
  );
}
