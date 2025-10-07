"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { FileText, Calendar, DollarSign, Store, Image as ImageIcon, Loader2, Eye, Download, Filter } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/components/ui/use-toast";
import { API_BASE } from "@/lib/utils";
import Image from "next/image";
import { ScrollArea } from "@/components/ui/scroll-area";
import ImageModal from "@/components/ImageModal";
import { downloadInvoiceAsPDF } from "@/lib/pdfUtils";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface Invoice {
  id: number;
  invoice_number: string;
  invoice_date: string;
  vendor: string;
  total_amount: string;
  category: string;
  ai_insight: string;
  invoice_type?: string;
  image_url?: string;
  created_at: string;
}

export default function InvoicesPage() {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [filteredInvoices, setFilteredInvoices] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedInvoice, setSelectedInvoice] = useState<Invoice | null>(null);
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [categoryFilter, setCategoryFilter] = useState<string>("all");
  const [pdfLoading, setPdfLoading] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    fetchInvoices();
  }, []);

  // Filter invoices when category changes - FIXED: No duplicates
  useEffect(() => {
    if (!invoices || invoices.length === 0) {
      setFilteredInvoices([]);
      return;
    }

    if (categoryFilter === "all") {
      setFilteredInvoices(invoices);
    } else {
      const filtered = invoices.filter((inv) => {
        // Check invoice_type first (more direct)
        if (inv.invoice_type?.trim() === categoryFilter.trim()) {
          return true;
        }
        
        // Fallback: check category.ar
        try {
          const cat = typeof inv.category === "string" ? JSON.parse(inv.category) : inv.category;
          return cat.ar?.trim() === categoryFilter.trim();
        } catch {
          return false;
        }
      });
      
      setFilteredInvoices(filtered);
    }
  }, [categoryFilter, invoices]);

  const fetchInvoices = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/invoices/all`);
      
      if (!response.ok) {
        throw new Error("فشل تحميل الفواتير");
      }
      
      const data = await response.json();
      
      // التأكد من أن البيانات مصفوفة
      if (Array.isArray(data)) {
        setInvoices(data);
        setFilteredInvoices(data);
      } else {
        console.error("❌ البيانات المستلمة ليست مصفوفة:", data);
        setInvoices([]);
        setFilteredInvoices([]);
      }
    } catch (error: any) {
      console.error("❌ خطأ في تحميل الفواتير:", error);
      setInvoices([]); // تعيين مصفوفة فارغة عند الخطأ
      toast({
        title: "خطأ",
        description: "فشل تحميل الفواتير",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const getCategoryArabic = (category: string) => {
    try {
      const cat = typeof category === "string" ? JSON.parse(category) : category;
      return cat.ar || "غير محدد";
    } catch {
      return "غير محدد";
    }
  };

  const handleDownloadPDF = async (invoice: Invoice) => {
    try {
      setPdfLoading(true);
      await downloadInvoiceAsPDF(invoice);
      toast({
        title: "تم التنزيل",
        description: "تم تنزيل الفاتورة كملف PDF بنجاح",
      });
    } catch (error) {
      console.error("Error downloading PDF:", error);
      toast({
        title: "خطأ",
        description: "فشل تنزيل الفاتورة",
        variant: "destructive",
      });
    } finally {
      setPdfLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center space-y-4"
        >
          <Loader2 className="w-12 h-12 animate-spin mx-auto text-primary" />
          <p className="text-muted-foreground">جاري تحميل الفواتير...</p>
        </motion.div>
      </div>
    );
  }

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
        className="space-y-6"
      >
        <div className="text-center space-y-4">
          <h1 className="text-5xl md:text-6xl font-black bg-gradient-to-l from-[#8dbcc7] to-[#d4a574] bg-clip-text text-transparent">
            الفواتير المرفوعة
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400">
            جميع الفواتير التي قمت برفعها مع صورها
          </p>
          <div className="inline-flex items-center gap-2 px-5 py-3 rounded-full bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl shadow-lg border border-[#8dbcc7]/20">
            <FileText className="w-5 h-5 text-[#8dbcc7]" />
            <span className="font-semibold">{filteredInvoices.length} من {invoices.length} فاتورة</span>
          </div>
        </div>

        {/* Filters - FIXED: Values match database exactly */}
        <div className="flex flex-wrap items-center justify-center gap-4" dir="rtl">
          <div className="flex items-center gap-2">
            <Filter className="w-4 h-4 text-muted-foreground" />
            <span className="text-sm font-medium text-muted-foreground">تصفية حسب:</span>
          </div>
          <Select value={categoryFilter} onValueChange={setCategoryFilter}>
            <SelectTrigger className="w-[200px]">
              <SelectValue placeholder="اختر الفئة" />
            </SelectTrigger>
            <SelectContent dir="rtl">
              <SelectItem value="all">الكل</SelectItem>
              <SelectItem value="مطعم">مطاعم</SelectItem>
              <SelectItem value="مقهى">مقاهي</SelectItem>
              <SelectItem value="صيدلية">صيدليات</SelectItem>
              <SelectItem value="تأمين">تأمين</SelectItem>
              <SelectItem value="شراء">شراء</SelectItem>
              <SelectItem value="خدمات">خدمات</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </motion.div>

      {/* Invoices Grid */}
      {filteredInvoices.length === 0 ? (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center py-12"
          dir="rtl"
        >
          <FileText className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
          <h3 className="text-xl font-semibold mb-2">
            {invoices.length === 0 ? "لا توجد فواتير" : "⚠️ لا توجد فواتير في هذه الفئة"}
          </h3>
          <p className="text-muted-foreground">
            {invoices.length === 0 ? "ابدأ برفع أول فاتورة!" : "جرب اختيار فئة أخرى أو اختر 'الكل'"}
          </p>
        </motion.div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredInvoices.map((invoice, index) => (
            <motion.div
              key={invoice.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
            >
              <Card className="overflow-hidden bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-0 shadow-xl hover:shadow-2xl transition-all duration-300 rounded-2xl group">
                {/* Invoice Image - Enhanced Arabic Layout */}
                <div 
                  className="relative h-80 w-full overflow-hidden rounded-t-xl bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-800 dark:to-gray-900 cursor-pointer"
                  onClick={() => invoice.image_url && setSelectedImage(invoice.image_url)}
                >
                  {invoice.image_url ? (
                    <>
                      <img
                        src={invoice.image_url}
                        alt={`فاتورة ${invoice.vendor}`}
                        className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                        onError={(e) => {
                          const target = e.target as HTMLImageElement;
                          target.src = '/placeholder-invoice.png';
                          target.onerror = () => {
                            target.style.display = 'none';
                            const fallback = document.getElementById(`fallback-${invoice.id}`);
                            if (fallback) fallback.style.display = 'flex';
                          };
                        }}
                      />
                      {/* Hover overlay with Eye icon */}
                      <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/0 to-black/30 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                        <div className="bg-white/90 dark:bg-black/80 rounded-full p-4 backdrop-blur-sm">
                          <Eye className="w-8 h-8 text-gray-800 dark:text-white" />
                        </div>
                      </div>
                    </>
                  ) : (
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="text-center text-gray-400">
                        <ImageIcon className="w-24 h-24 mx-auto mb-3 opacity-50" />
                        <p className="text-sm font-medium">لا توجد صورة</p>
                      </div>
                    </div>
                  )}
                  
                  {/* Fallback if image fails */}
                  <div 
                    id={`fallback-${invoice.id}`}
                    className="absolute inset-0 items-center justify-center hidden"
                  >
                    <div className="text-center text-gray-400">
                      <ImageIcon className="w-24 h-24 mx-auto mb-3 opacity-50" />
                      <p className="text-sm font-medium">فشل تحميل الصورة</p>
                    </div>
                  </div>
                  
                  {/* Invoice Type Badge - Top Right */}
                  {invoice.invoice_type && invoice.invoice_type !== "غير محدد" && (
                    <div className="absolute top-3 right-3 px-3 py-1.5 rounded-full bg-gradient-to-r from-purple-500 to-pink-600 text-white text-xs font-bold shadow-lg backdrop-blur-sm" dir="rtl">
                      {invoice.invoice_type}
                    </div>
                  )}
                  
                  {/* Category Badge - Below Invoice Type */}
                  <div className="absolute top-12 right-3 px-3 py-1 rounded-full bg-gradient-to-r from-blue-500 to-cyan-500 text-white text-xs font-medium shadow-md backdrop-blur-sm" dir="rtl">
                    {getCategoryArabic(invoice.category)}
                  </div>
                  
                  {/* Invoice Number Badge - Top Left */}
                  {invoice.invoice_number && (
                    <div className="absolute top-3 left-3 px-2 py-1 rounded-md bg-white/95 dark:bg-black/80 text-xs font-semibold backdrop-blur-sm shadow-md" dir="ltr">
                      #{invoice.invoice_number}
                    </div>
                  )}
                </div>

                <CardHeader dir="rtl">
                  <CardTitle className="text-lg flex items-center gap-2">
                    <Store className="w-5 h-5 text-blue-600" />
                    {invoice.vendor || "متجر غير معروف"}
                  </CardTitle>
                  <CardDescription className="flex flex-col gap-1.5 mt-2">
                    {/* نوع الفاتورة */}
                    {invoice.invoice_type && invoice.invoice_type !== "غير محدد" && (
                      <span className="flex items-center gap-2 text-purple-600 dark:text-purple-400 font-medium">
                        <span className="w-2 h-2 bg-purple-500 rounded-full" />
                        {invoice.invoice_type}
                      </span>
                    )}
                    
                    {/* رقم الفاتورة */}
                    <span className="flex items-center gap-1.5">
                      <FileText className="w-3.5 h-3.5" />
                      <span className="text-sm">
                        رقم الفاتورة: {invoice.invoice_number || "لا يوجد رقم"}
                      </span>
                    </span>
                    
                    {/* التاريخ */}
                    <span className="flex items-center gap-1.5">
                      <Calendar className="w-3.5 h-3.5" />
                      <span className="text-sm">
                        {invoice.invoice_date
                          ? new Date(invoice.invoice_date).toLocaleDateString("ar-SA", {
                              year: "numeric",
                              month: "long",
                              day: "numeric"
                            })
                          : "تاريخ غير محدد"}
                      </span>
                    </span>
                  </CardDescription>
                </CardHeader>

                <CardContent>
                  <div className="space-y-3">
                    {/* Total Amount */}
                    <div className="flex items-center justify-between p-3 rounded-lg bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800">
                      <span className="text-sm font-medium text-green-700 dark:text-green-300">
                        الإجمالي
                      </span>
                      <span className="text-xl font-bold text-green-600 dark:text-green-400">
                        {invoice.total_amount} ر.س
                      </span>
                    </div>

                    {/* AI Insight Preview */}
                    {invoice.ai_insight && invoice.ai_insight !== "Not Mentioned" && (
                      <div className="p-3 rounded-lg bg-purple-50 dark:bg-purple-950 border border-purple-200 dark:border-purple-800">
                        <p className="text-xs text-purple-700 dark:text-purple-300 line-clamp-2">
                          💡 {invoice.ai_insight}
                        </p>
                      </div>
                    )}

                    {/* Created Date */}
                    <div className="text-xs text-muted-foreground text-center pt-2 border-t">
                      تم الرفع: {new Date(invoice.created_at).toLocaleDateString("ar-SA")}
                    </div>

                    {/* PDF Download Button */}
                    <Button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDownloadPDF(invoice);
                      }}
                      disabled={pdfLoading}
                      className="w-full mt-3"
                      variant="outline"
                      dir="rtl"
                    >
                      <Download className="w-4 h-4 ml-2" />
                      {pdfLoading ? "جاري التنزيل..." : "تحميل كـ PDF"}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      )}

      {/* Image Modal */}
      <ImageModal
        imageUrl={selectedImage}
        onClose={() => setSelectedImage(null)}
        title="معاينة الفاتورة"
      />
    </div>
    </main>
    </div>
  );
}

