"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useTheme } from "next-themes";
import Image from "next/image";
import {
  BarChart3,
  FileText,
  DollarSign,
  TrendingUp,
  Store,
  Loader2,
  Sparkles,
  Calendar,
  CreditCard,
  Receipt,
  TrendingDown,
  Percent,
  Filter as FilterIcon,
  ShoppingBag,
  CheckCircle2,
  Clock,
  PieChartIcon,
} from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/components/ui/use-toast";
import { API_BASE } from "@/lib/utils";
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from "recharts";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface Invoice {
  id: number;
  vendor: string;
  invoice_number?: string;
  invoice_date: string;
  invoice_type?: string;
  total_amount: string;
  tax?: string;
  payment_method?: string;
  category: string;
  created_at: string;
  ai_insight?: string;
}

// Soft, pastel Arabic-friendly colors
const COLORS = ['#60a5fa', '#34d399', '#fbbf24', '#f87171', '#a78bfa', '#ec4899', '#06b6d4', '#84cc16'];

export default function DashboardPage() {
  const [loading, setLoading] = useState(true);
  const [filterLoading, setFilterLoading] = useState(false);
  const [stats, setStats] = useState<any>(null);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [filteredInvoices, setFilteredInvoices] = useState<Invoice[]>([]);
  
  // Filters
  const [categoryFilter, setCategoryFilter] = useState<string>("all");
  const [monthFilter, setMonthFilter] = useState<string>("all");
  const [paymentFilter, setPaymentFilter] = useState<string>("all");
  
  const { toast } = useToast();
  const { theme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    fetchData();
  }, []);

  // Apply filters when any filter changes
  useEffect(() => {
    applyFilters();
  }, [categoryFilter, monthFilter, paymentFilter, invoices]);

  const fetchData = async () => {
    try {
      setLoading(true);

      const [statsResponse, invoicesResponse] = await Promise.all([
        fetch(`${API_BASE}/dashboard/stats`),
        fetch(`${API_BASE}/invoices/all`),
      ]);

      const statsData = await statsResponse.json();
      const invoicesData = await invoicesResponse.json();

      setStats(statsData);
      setInvoices(Array.isArray(invoicesData) ? invoicesData : []);
      setFilteredInvoices(Array.isArray(invoicesData) ? invoicesData : []);
    } catch (error: any) {
      toast({
        title: "خطأ",
        description: "فشل تحميل البيانات",
        variant: "destructive",
      });
      setInvoices([]);
      setFilteredInvoices([]);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = async () => {
    setFilterLoading(true);
    
    // Simulate smooth UX delay
    await new Promise(resolve => setTimeout(resolve, 300));
    
    let filtered = [...invoices];

    // 1. Category filter
    if (categoryFilter !== "all") {
      filtered = filtered.filter((inv) => {
        if (inv.invoice_type?.trim() === categoryFilter.trim()) {
          return true;
        }
        try {
          const cat = typeof inv.category === "string" ? JSON.parse(inv.category) : inv.category;
          return cat.ar?.trim() === categoryFilter.trim();
        } catch {
          return false;
        }
      });
    }

    // 2. Month filter
    if (monthFilter !== "all") {
      filtered = filtered.filter((inv) => {
        if (!inv.invoice_date) return false;
        const invMonth = new Date(inv.invoice_date).getMonth();
        return invMonth === parseInt(monthFilter);
      });
    }

    // 3. Payment method filter
    if (paymentFilter !== "all") {
      filtered = filtered.filter((inv) => 
        inv.payment_method?.toLowerCase().includes(paymentFilter.toLowerCase())
      );
    }

    setFilteredInvoices(filtered);
    setFilterLoading(false);
  };

  // 🧠 SMART INSIGHTS GENERATOR
  const generateSmartInsights = (): Array<{icon: string, label: string, value: string, trend?: 'up' | 'down' | 'neutral'}> => {
    const insights: Array<{icon: string, label: string, value: string, trend?: 'up' | 'down' | 'neutral'}> = [];
    
    if (filteredInvoices.length === 0) {
      return [{icon: "📊", label: "البيانات", value: "لا توجد بيانات كافية لتوليد رؤى", trend: 'neutral'}];
    }

    // Month-over-month growth
    const now = new Date();
    const currentMonth = now.toLocaleDateString("ar", { month: "long", year: "numeric" });
    const lastMonthDate = new Date(now.getFullYear(), now.getMonth() - 1, 1);
    const previousMonth = lastMonthDate.toLocaleDateString("ar", { month: "long", year: "numeric" });
    
    const thisMonth = filteredInvoices.filter(inv => {
      const date = new Date(inv.invoice_date);
      return date.getMonth() === now.getMonth() && date.getFullYear() === now.getFullYear();
    });
    
    const lastMonth = filteredInvoices.filter(inv => {
      const date = new Date(inv.invoice_date);
      return date.getMonth() === lastMonthDate.getMonth() && date.getFullYear() === lastMonthDate.getFullYear();
    });

    const thisMonthTotal = thisMonth.reduce((sum, inv) => sum + parseFloat(inv.total_amount || "0"), 0);
    const lastMonthTotal = lastMonth.reduce((sum, inv) => sum + parseFloat(inv.total_amount || "0"), 0);

    if (lastMonthTotal > 0) {
      const growth = ((thisMonthTotal - lastMonthTotal) / lastMonthTotal) * 100;
      const trend = growth > 0 ? 'up' : growth < 0 ? 'down' : 'neutral';
      insights.push({
        icon: trend === 'up' ? '📈' : '📉',
        label: `المقارنة الشهرية (${currentMonth} مقابل ${previousMonth})`,
        value: `${growth > 0 ? 'زيادة' : 'انخفاض'} بنسبة ${Math.abs(growth).toFixed(1)}٪ - إجمالي ${thisMonthTotal.toFixed(2)} ر.س`,
        trend: trend
      });
    } else if (thisMonthTotal > 0) {
      insights.push({
        icon: '📊',
        label: `الإنفاق الشهري (${currentMonth})`,
        value: `${thisMonthTotal.toFixed(2)} ر.س - ${thisMonth.length} ${thisMonth.length === 1 ? 'فاتورة' : 'فواتير'}`,
        trend: 'neutral'
      });
    }

    // Top vendor
    const vendorCount = filteredInvoices.reduce((acc: any, inv) => {
      const vendor = inv.vendor || "غير معروف";
      acc[vendor] = (acc[vendor] || 0) + 1;
      return acc;
    }, {});
    
    const topVendor = Object.entries(vendorCount).sort((a: any, b: any) => b[1] - a[1])[0];
    if (topVendor) {
      insights.push({
        icon: '🏪',
        label: 'المتجر الأكثر تعاملاً',
        value: `${topVendor[0]} - ${topVendor[1]} ${topVendor[1] === 1 ? 'فاتورة' : 'فواتير'}`,
        trend: 'neutral'
      });
    }

    // Average spending
    const avgSpending = filteredInvoices.reduce((sum, inv) => sum + parseFloat(inv.total_amount || "0"), 0) / filteredInvoices.length;
    insights.push({
      icon: '💵',
      label: 'متوسط قيمة الفاتورة',
      value: `${avgSpending.toFixed(2)} ر.س`,
      trend: 'neutral'
    });

    // Most expensive category
    const categoryTotals = filteredInvoices.reduce((acc: any, inv) => {
      const type = inv.invoice_type || "أخرى";
      acc[type] = (acc[type] || 0) + parseFloat(inv.total_amount || "0");
      return acc;
    }, {});
    
    const topCategory = Object.entries(categoryTotals).sort((a: any, b: any) => b[1] - a[1])[0];
    if (topCategory) {
      const percentage = ((topCategory[1] as number) / filteredInvoices.reduce((sum, inv) => sum + parseFloat(inv.total_amount || "0"), 0) * 100).toFixed(0);
      insights.push({
        icon: '🎯',
        label: 'الفئة الأكثر إنفاقاً',
        value: `${topCategory[0]} - ${(topCategory[1] as number).toFixed(2)} ر.س (${percentage}٪)`,
        trend: 'neutral'
      });
    }

    // Most used payment method
    const paymentCount = filteredInvoices.reduce((acc: any, inv) => {
      const method = inv.payment_method || "غير محدد";
      acc[method] = (acc[method] || 0) + 1;
      return acc;
    }, {});
    
    const topPayment = Object.entries(paymentCount).sort((a: any, b: any) => b[1] - a[1])[0];
    if (topPayment) {
      const percentage = ((topPayment[1] as number) / filteredInvoices.length * 100).toFixed(0);
      insights.push({
        icon: '💳',
        label: 'طريقة الدفع المفضلة',
        value: `${topPayment[0]} - ${percentage}٪ من المعاملات`,
        trend: 'neutral'
      });
    }

    // Busiest day (with Gregorian calendar)
    const dayCount = filteredInvoices.reduce((acc: any, inv) => {
      if (!inv.invoice_date) return acc;
      const day = new Date(inv.invoice_date).toLocaleDateString("ar", { weekday: "long" });
      acc[day] = (acc[day] || 0) + 1;
      return acc;
    }, {});
    
    const busiestDay = Object.entries(dayCount).sort((a: any, b: any) => b[1] - a[1])[0];
    if (busiestDay) {
      insights.push({
        icon: '📅',
        label: 'اليوم الأكثر نشاطاً',
        value: `${busiestDay[0]} - ${busiestDay[1]} ${busiestDay[1] === 1 ? 'فاتورة' : 'فواتير'}`,
        trend: 'neutral'
      });
    }

    return insights;
  };

  if (loading) {
    return (
      <div className="animated-bg min-h-screen flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center space-y-4"
          dir="rtl"
        >
          <Loader2 className="w-16 h-16 animate-spin mx-auto text-primary" />
          <p className="text-lg font-medium">جاري تحميل لوحة التحكم...</p>
          <p className="text-sm text-muted-foreground">نحلل بياناتك...</p>
        </motion.div>
      </div>
    );
  }

  // Calculate analytics from filtered invoices
  const totalTax = filteredInvoices.reduce((sum, inv) => sum + parseFloat(inv.tax || "0"), 0);
  const totalSpent = filteredInvoices.reduce((sum, inv) => sum + parseFloat(inv.total_amount || "0"), 0);
  const avgInvoice = filteredInvoices.length > 0 ? totalSpent / filteredInvoices.length : 0;
  const maxInvoice = filteredInvoices.length > 0 ? Math.max(...filteredInvoices.map(inv => parseFloat(inv.total_amount || "0"))) : 0;
  const minInvoice = filteredInvoices.length > 0 ? Math.min(...filteredInvoices.map(inv => parseFloat(inv.total_amount || "0"))) : 0;

  // Category data for pie chart
  const categoryData = filteredInvoices.reduce((acc: any, invoice: Invoice) => {
    let category = "أخرى";
    try {
      const cat = typeof invoice.category === "string" ? JSON.parse(invoice.category) : invoice.category;
      category = cat.ar || invoice.invoice_type || "أخرى";
    } catch (e) {
      category = invoice.invoice_type || "أخرى";
    }

    if (!acc[category]) {
      acc[category] = { name: category, value: 0, count: 0 };
    }
    acc[category].count += 1;
    acc[category].value += parseFloat(invoice.total_amount || "0");
    return acc;
  }, {});

  const categoryChartData = Object.values(categoryData);

  // Monthly data (Gregorian calendar)
  const monthlyData = filteredInvoices.reduce((acc: any, invoice: Invoice) => {
    if (!invoice.invoice_date) return acc;
    
    const date = new Date(invoice.invoice_date);
    const monthKey = date.toLocaleDateString("ar", { month: "short", year: "numeric" });
    
    if (!acc[monthKey]) {
      acc[monthKey] = { month: monthKey, total: 0, count: 0, tax: 0 };
    }
    
    acc[monthKey].total += parseFloat(invoice.total_amount || "0");
    acc[monthKey].count += 1;
    acc[monthKey].tax += parseFloat(invoice.tax || "0");
    return acc;
  }, {});

  const monthlyChartData = Object.values(monthlyData).slice(-6);

  // Payment method data
  const paymentMethodData = filteredInvoices.reduce((acc: any, invoice: Invoice) => {
    const method = invoice.payment_method || "غير محدد";
    if (!acc[method]) {
      acc[method] = { name: method, value: 0, count: 0 };
    }
    acc[method].count += 1;
    acc[method].value += parseFloat(invoice.total_amount || "0");
    return acc;
  }, {});

  const paymentChartData = Object.values(paymentMethodData);

  // Day data for radar chart (Gregorian calendar)
  const dayData = filteredInvoices.reduce((acc: any, invoice: Invoice) => {
    if (!invoice.invoice_date) return acc;
    
    const day = new Date(invoice.invoice_date).toLocaleDateString("ar", { weekday: "long" });
    
    if (!acc[day]) {
      acc[day] = { day: day, total: 0, count: 0 };
    }
    
    acc[day].total += parseFloat(invoice.total_amount || "0");
    acc[day].count += 1;
    return acc;
  }, {});

  const dayChartData = Object.values(dayData);

  const statCards = [
    {
      title: "إجمالي الفواتير",
      value: filteredInvoices.length,
      icon: FileText,
      color: "from-blue-500 to-cyan-500",
      suffix: "فاتورة",
    },
    {
      title: "إجمالي الإنفاق",
      value: totalSpent.toFixed(2),
      icon: DollarSign,
      color: "from-green-500 to-emerald-500",
      suffix: "ر.س",
    },
    {
      title: "متوسط الفاتورة",
      value: avgInvoice.toFixed(2),
      icon: TrendingUp,
      color: "from-purple-500 to-pink-500",
      suffix: "ر.س",
    },
    {
      title: "إجمالي الضرائب",
      value: totalTax.toFixed(2),
      icon: Receipt,
      color: "from-indigo-500 to-purple-500",
      suffix: "ر.س",
    },
  ];

  const smartInsights = generateSmartInsights();

  return (
    <div className="relative min-h-screen">
      {/* Fixed Animated Background */}
      <div className="fixed inset-0 -z-10 animate-gradient opacity-90" />
      
      <main className="container mx-auto px-6 md:px-16 lg:px-24 xl:px-32 py-20 md:py-24">
      <div className="space-y-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center space-y-8 py-4"
          dir="rtl"
        >
          <div className="flex justify-center mb-4">
            {mounted && (
              <Image
                src={theme === "dark" ? "/title-dashboard-dark.svg" : "/title-dashboard.svg"}
                alt="لوحة التحكم الذكية"
                width={600}
                height={120}
                className="w-full max-w-2xl h-auto"
                priority
              />
            )}
            {!mounted && (
              <Image
                src="/title-dashboard.svg"
                alt="لوحة التحكم الذكية"
                width={600}
                height={120}
                className="w-full max-w-2xl h-auto"
                priority
              />
            )}
          </div>
          <p className="text-xl md:text-2xl text-gray-700 dark:text-gray-300 max-w-3xl mx-auto font-bold leading-relaxed tracking-wide">
            تحليل شامل لمصاريفك وفواتيرك مع رؤى تفصيلية
          </p>
        </motion.div>

        {/* Filters Bar */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <Card className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-0 shadow-xl rounded-2xl">
            <CardContent className="pt-6">
              <div className="flex flex-wrap items-center justify-center gap-4" dir="rtl">
                <div className="flex items-center gap-2">
                  <FilterIcon className="w-5 h-5 text-primary" />
                  <span className="font-semibold text-base md:text-lg">تصفية البيانات:</span>
                </div>

                <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                  <SelectTrigger className="w-[160px]">
                    <SelectValue placeholder="فئة المتجر" />
                  </SelectTrigger>
                  <SelectContent dir="rtl">
                    <SelectItem value="all">كل الفئات</SelectItem>
                    <SelectItem value="مطعم">مطاعم</SelectItem>
                    <SelectItem value="مقهى">مقاهي</SelectItem>
                    <SelectItem value="صيدلية">صيدليات</SelectItem>
                    <SelectItem value="تأمين">تأمين</SelectItem>
                    <SelectItem value="شراء">شراء</SelectItem>
                  </SelectContent>
                </Select>

                <Select value={monthFilter} onValueChange={setMonthFilter}>
                  <SelectTrigger className="w-[160px]">
                    <SelectValue placeholder="الشهر" />
                  </SelectTrigger>
                  <SelectContent dir="rtl">
                    <SelectItem value="all">كل الأشهر</SelectItem>
                    <SelectItem value="0">يناير</SelectItem>
                    <SelectItem value="1">فبراير</SelectItem>
                    <SelectItem value="2">مارس</SelectItem>
                    <SelectItem value="3">أبريل</SelectItem>
                    <SelectItem value="4">مايو</SelectItem>
                    <SelectItem value="5">يونيو</SelectItem>
                    <SelectItem value="6">يوليو</SelectItem>
                    <SelectItem value="7">أغسطس</SelectItem>
                    <SelectItem value="8">سبتمبر</SelectItem>
                    <SelectItem value="9">أكتوبر</SelectItem>
                    <SelectItem value="10">نوفمبر</SelectItem>
                    <SelectItem value="11">ديسمبر</SelectItem>
                  </SelectContent>
                </Select>

                <Select value={paymentFilter} onValueChange={setPaymentFilter}>
                  <SelectTrigger className="w-[160px]">
                    <SelectValue placeholder="طريقة الدفع" />
                  </SelectTrigger>
                  <SelectContent dir="rtl">
                    <SelectItem value="all">كل الطرق</SelectItem>
                    <SelectItem value="visa">Visa</SelectItem>
                    <SelectItem value="mada">Mada</SelectItem>
                    <SelectItem value="mastercard">MasterCard</SelectItem>
                    <SelectItem value="cash">نقدًا</SelectItem>
                  </SelectContent>
                </Select>

                {filterLoading && (
                  <div className="flex items-center gap-2 text-primary">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span className="text-sm">جاري تحديث البيانات...</span>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* KPI Stats Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
          {statCards.map((stat, index) => (
            <motion.div
              key={stat.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 + index * 0.05 }}
            >
              <Card className="rounded-2xl bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-0 shadow-xl hover:shadow-2xl p-4 transition-all duration-500">
                <CardContent className="p-0">
                  <div className="flex items-start justify-between" dir="rtl">
                    <div className="space-y-2 flex-1">
                      <p className="text-xs md:text-sm text-muted-foreground">{stat.title}</p>
                      <div className="flex items-baseline gap-2">
                        <p className="text-2xl md:text-3xl font-bold">{stat.value}</p>
                        <p className="text-xs md:text-sm text-muted-foreground">{stat.suffix}</p>
                      </div>
                    </div>
                    <div className={`w-12 h-12 md:w-14 md:h-14 rounded-xl bg-gradient-to-br ${stat.color} flex items-center justify-center shadow-lg`}>
                      <stat.icon className="w-6 h-6 md:w-7 md:h-7 text-white" />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Main Dashboard Layout - 2 Column Responsive */}
        <div className="grid gap-6 lg:grid-cols-2">
          
          {/* Column 1: Category Pie Chart + Day Radar Chart */}
          <div className="space-y-6">
            
            {/* Category Spending Pie Chart - FIXED */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
            >
              <Card className="rounded-2xl bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-0 shadow-xl hover:shadow-2xl transition-all duration-500">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-base md:text-lg" dir="rtl">
                    <PieChartIcon className="w-5 h-5" />
                    توزيع المصروفات حسب التصنيف
                  </CardTitle>
                  <CardDescription className="text-sm" dir="rtl">
                    تحليل الإنفاق حسب نوع النشاط التجاري
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {categoryChartData.length > 0 ? (
                    <>
                      <ResponsiveContainer width="100%" height={350}>
                        <PieChart>
                          <Pie
                            data={categoryChartData}
                            cx="50%"
                            cy="50%"
                            outerRadius={90}
                            innerRadius={50}
                            dataKey="value"
                            nameKey="name"
                            paddingAngle={2}
                          >
                            {categoryChartData.map((entry: any, index: number) => (
                              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                            ))}
                          </Pie>
                          <Tooltip 
                            formatter={(value: any) => `${value.toFixed(2)} ر.س`}
                            contentStyle={{ 
                              backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                              borderRadius: '8px', 
                              border: 'none', 
                              boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                              direction: 'rtl',
                              fontSize: '14px',
                            }}
                          />
                        </PieChart>
                      </ResponsiveContainer>
                      
                      {/* Legend Below Chart */}
                      <div className="mt-4 grid grid-cols-2 gap-3" dir="rtl">
                        {categoryChartData.map((entry: any, index: number) => (
                          <div key={index} className="flex items-center gap-2">
                            <div 
                              className="w-4 h-4 rounded-full flex-shrink-0"
                              style={{ backgroundColor: COLORS[index % COLORS.length] }}
                            />
                            <div className="flex-1 min-w-0">
                              <p className="text-sm font-medium truncate">{entry.name}</p>
                              <p className="text-xs text-muted-foreground">
                                {entry.value.toFixed(2)} ر.س
                              </p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </>
                  ) : (
                    <div className="h-[350px] flex items-center justify-center text-muted-foreground" dir="rtl">
                      <p className="text-sm">لا توجد بيانات لعرضها</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </motion.div>

            {/* Day Radar Chart */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5 }}
            >
              <Card className="rounded-2xl bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-0 shadow-xl hover:shadow-2xl transition-all duration-500">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-base md:text-lg" dir="rtl">
                    <Clock className="w-5 h-5" />
                    الإنفاق حسب اليوم
                  </CardTitle>
                  <CardDescription className="text-sm" dir="rtl">
                    أي يوم تنفق أكثر؟
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {dayChartData.length > 0 ? (
                    <ResponsiveContainer width="100%" height={300}>
                      <RadarChart data={dayChartData}>
                        <PolarGrid stroke="#e5e7eb" />
                        <PolarAngleAxis dataKey="day" tick={{ fontSize: 11 }} />
                        <PolarRadiusAxis tick={{ fontSize: 11 }} />
                        <Radar name="الإنفاق" dataKey="total" stroke="#10b981" fill="#10b981" fillOpacity={0.6} />
                        <Tooltip 
                          formatter={(value: any) => `${value.toFixed(2)} ر.س`}
                          contentStyle={{ 
                            backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                            borderRadius: '8px', 
                            border: 'none', 
                            boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                            direction: 'rtl',
                          }}
                        />
                      </RadarChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="h-[300px] flex items-center justify-center text-muted-foreground" dir="rtl">
                      <p className="text-sm">لا توجد بيانات لعرضها</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          </div>

          {/* Column 2: Monthly Trend + Payment Methods */}
          <div className="space-y-6">
            
            {/* Monthly Spending Trend */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
            >
              <Card className="rounded-2xl bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-0 shadow-xl hover:shadow-2xl transition-all duration-500">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-base md:text-lg" dir="rtl">
                    <Calendar className="w-5 h-5" />
                    الاتجاه الشهري للإنفاق
                  </CardTitle>
                  <CardDescription className="text-sm" dir="rtl">
                    تتبع الإنفاق عبر الأشهر
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {monthlyChartData.length > 0 ? (
                    <ResponsiveContainer width="100%" height={300}>
                      <AreaChart data={monthlyChartData}>
                        <defs>
                          <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                            <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.1}/>
                          </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
                        <XAxis dataKey="month" tick={{ fontSize: 10 }} />
                        <YAxis tick={{ fontSize: 10 }} />
                        <Tooltip 
                          formatter={(value: any) => `${value.toFixed(2)} ر.س`}
                          contentStyle={{ 
                            backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                            borderRadius: '8px', 
                            border: 'none', 
                            boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                            direction: 'rtl',
                          }}
                        />
                        <Area type="monotone" dataKey="total" stroke="#3b82f6" strokeWidth={2} fillOpacity={1} fill="url(#colorTotal)" />
                      </AreaChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="h-[300px] flex items-center justify-center text-muted-foreground" dir="rtl">
                      <p className="text-sm">لا توجد بيانات لعرضها</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </motion.div>

            {/* Payment Methods Bar Chart */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5 }}
            >
              <Card className="rounded-2xl bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-0 shadow-xl hover:shadow-2xl transition-all duration-500">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-base md:text-lg" dir="rtl">
                    <CreditCard className="w-5 h-5" />
                    طرق الدفع
                  </CardTitle>
                  <CardDescription className="text-sm" dir="rtl">
                    توزيع المدفوعات حسب الطريقة
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {paymentChartData.length > 0 ? (
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={paymentChartData}>
                        <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
                        <XAxis dataKey="name" tick={{ fontSize: 10 }} />
                        <YAxis tick={{ fontSize: 10 }} />
                        <Tooltip 
                          formatter={(value: any) => `${value.toFixed(2)} ر.س`}
                          contentStyle={{ 
                            backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                            borderRadius: '8px', 
                            border: 'none', 
                            boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                            direction: 'rtl',
                          }}
                        />
                        <Bar dataKey="value" fill="#a78bfa" radius={[8, 8, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="h-[300px] flex items-center justify-center text-muted-foreground" dir="rtl">
                      <p className="text-sm">لا توجد بيانات لعرضها</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </div>

        {/* Smart Insights Section - Enhanced */}
        <AnimatePresence>
          {filteredInvoices.length > 0 && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ delay: 0.6 }}
            >
              <Card className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-0 shadow-xl hover:shadow-2xl transition-all duration-500 rounded-2xl overflow-hidden">
                <CardHeader className="bg-gradient-to-r from-purple-500/10 to-pink-500/10 dark:from-purple-500/20 dark:to-pink-500/20 pb-4">
                  <CardTitle className="flex items-center gap-3 text-xl md:text-2xl" dir="rtl">
                    <Sparkles className="w-7 h-7 text-purple-600 dark:text-purple-400 animate-pulse" />
                    رؤى ذكية متقدمة
                  </CardTitle>
                  <CardDescription className="text-sm" dir="rtl">
                    تحليل شامل لبياناتك المالية
                  </CardDescription>
                </CardHeader>
                <CardContent className="pt-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4" dir="rtl">
                    {smartInsights.map((insight, index) => {
                      // Map icons to Lucide components
                      const IconComponent = 
                        insight.icon === '📈' || insight.icon === '📉' || insight.icon === '📊' ? Calendar :
                        insight.icon === '🏪' ? Store :
                        insight.icon === '💵' || insight.icon === '💰' ? DollarSign :
                        insight.icon === '🎯' ? ShoppingBag :
                        insight.icon === '💳' ? CreditCard :
                        insight.icon === '📅' ? Clock :
                        Receipt;
                      
                      return (
                        <motion.div
                          key={index}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.7 + index * 0.05 }}
                          className={`relative p-5 rounded-xl border ${
                            insight.trend === 'up' 
                              ? 'bg-gradient-to-br from-orange-50 to-red-50 dark:from-orange-950/30 dark:to-red-950/30 border-orange-300 dark:border-orange-700' 
                              : insight.trend === 'down' 
                              ? 'bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-950/30 dark:to-emerald-950/30 border-green-300 dark:border-green-700' 
                              : 'bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/30 dark:to-indigo-950/30 border-blue-300 dark:border-blue-700'
                          } backdrop-blur-sm hover:shadow-lg hover:scale-[1.02] transition-all duration-300`}
                        >
                          {/* Icon & Trend Indicator */}
                          <div className="flex items-start justify-between mb-4">
                            <div className={`p-3 rounded-lg ${
                              insight.trend === 'up' 
                                ? 'bg-orange-100 dark:bg-orange-900/50' 
                                : insight.trend === 'down' 
                                ? 'bg-green-100 dark:bg-green-900/50' 
                                : 'bg-blue-100 dark:bg-blue-900/50'
                            }`}>
                              <IconComponent className={`w-6 h-6 ${
                                insight.trend === 'up' 
                                  ? 'text-orange-600 dark:text-orange-400' 
                                  : insight.trend === 'down' 
                                  ? 'text-green-600 dark:text-green-400' 
                                  : 'text-blue-600 dark:text-blue-400'
                              }`} />
                            </div>
                            {insight.trend === 'up' && (
                              <div className="flex items-center gap-1 px-2 py-1 rounded-full bg-orange-100 dark:bg-orange-900/50">
                                <TrendingUp className="w-4 h-4 text-orange-600 dark:text-orange-400" />
                                <span className="text-xs font-bold text-orange-600 dark:text-orange-400">زيادة</span>
                              </div>
                            )}
                            {insight.trend === 'down' && (
                              <div className="flex items-center gap-1 px-2 py-1 rounded-full bg-green-100 dark:bg-green-900/50">
                                <TrendingDown className="w-4 h-4 text-green-600 dark:text-green-400" />
                                <span className="text-xs font-bold text-green-600 dark:text-green-400">انخفاض</span>
                              </div>
                            )}
                          </div>
                          
                          {/* Label */}
                          <h4 className="text-xs font-semibold text-foreground/60 mb-2 uppercase tracking-wide">
                            {insight.label}
                          </h4>
                          
                          {/* Value */}
                          <p className="text-lg font-bold text-foreground leading-relaxed">
                            {insight.value}
                          </p>
                        </motion.div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Top Vendors Section */}
        {stats?.top_vendors && stats.top_vendors.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
          >
            <Card className="rounded-xl shadow-md hover:shadow-lg bg-white/80 dark:bg-gray-900/60 transition-all duration-500">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base md:text-lg" dir="rtl">
                  <Store className="w-5 h-5" />
                  أكثر المتاجر تكرارًا
                </CardTitle>
                <CardDescription className="text-sm" dir="rtl">
                  المتاجر التي تتعامل معها بشكل متكرر
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {stats.top_vendors.slice(0, 6).map((vendor: any, index: number) => (
                    <motion.div
                      key={vendor.vendor}
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 0.9 + index * 0.05 }}
                      className="flex items-center gap-3 p-4 rounded-xl bg-gradient-to-br from-gray-50/80 to-gray-100/80 dark:from-gray-800/80 dark:to-gray-900/80 hover:shadow-lg transition-all duration-300 backdrop-blur-sm"
                      dir="rtl"
                    >
                      <div 
                        className="w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-lg shadow-md"
                        style={{ background: `linear-gradient(135deg, ${COLORS[index % COLORS.length]}, ${COLORS[(index + 1) % COLORS.length]})` }}
                      >
                        {index + 1}
                      </div>
                      <div className="flex-1">
                        <p className="font-bold text-sm md:text-base">{vendor.vendor || "متجر غير معروف"}</p>
                        <p className="text-xs md:text-sm text-muted-foreground">
                          {vendor.count} {vendor.count === 1 ? "فاتورة" : "فواتير"}
                        </p>
                      </div>
                      <Store className="w-5 h-5 text-primary" />
                    </motion.div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </div>
      </main>
    </div>
  );
}
