"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Upload, Camera, FileImage, CheckCircle, XCircle, Loader2, Save, Edit2, Copy } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { useToast } from "@/components/ui/use-toast";
import { API_BASE } from "@/lib/utils";
import InvoiceResultCard from "@/components/InvoiceResultCard";
import Image from "next/image";
import { useTheme } from "next-themes";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

interface ItemData {
  description: string;
  quantity: number;
  unit_price: number;
  total: number;
}

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [progress, setProgress] = useState(0);
  const [progressMessage, setProgressMessage] = useState("");
  const [extractedData, setExtractedData] = useState<any>(null);
  const [editableData, setEditableData] = useState<any>(null);
  const [items, setItems] = useState<ItemData[]>([]);
  const [result, setResult] = useState<any>(null);
  const [imageUrl, setImageUrl] = useState<string>("");
  const [errorDialogOpen, setErrorDialogOpen] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [mounted, setMounted] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    setMounted(true);
  }, []);

  // Prevent hydration mismatch
  if (!mounted) {
    return null;
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'application/pdf'];
      if (!validTypes.includes(selectedFile.type)) {
        toast({
          title: "نوع ملف غير مدعوم",
          description: "الرجاء اختيار صورة (JPG, PNG) أو ملف PDF",
          variant: "destructive",
        });
        return;
      }
      setFile(selectedFile);
      setResult(null);
      setExtractedData(null);
      setEditableData(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      toast({
        title: "خطأ",
        description: "الرجاء اختيار صورة أو ملف PDF للفاتورة أولاً",
        variant: "destructive",
      });
      return;
    }

    try {
      // Step 1: Upload and Auto-Fix
      setUploading(true);
      setProgress(5);
      setProgressMessage("📤 جاري رفع الفاتورة...");

      const formData = new FormData();
      formData.append("file", file);

      const uploadResponse = await fetch(`${API_BASE}/upload/`, {
        method: "POST",
        body: formData,
      });

      if (!uploadResponse.ok) {
        const errorData = await uploadResponse.json().catch(() => ({}));
        const errorMessage = errorData.detail || uploadResponse.statusText || "فشل رفع الملف";
        console.error("Upload error:", errorMessage);
        throw new Error(errorMessage);
      }

      setProgress(20);
      setProgressMessage("🔧 جاري تحسين جودة الصورة...");
      
      // محاكاة وقت المعالجة (Backend يعالج الصورة)
      await new Promise(resolve => setTimeout(resolve, 800));

      const uploadData = await uploadResponse.json();
      const uploadedImageUrl = uploadData.url;
      setImageUrl(uploadedImageUrl);
      
      if (uploadData.converted_from_pdf) {
        toast({
          title: "تم التحويل ✅",
          description: "تم تحويل ملف PDF إلى صورة بنجاح",
        });
      }

      setProgress(45);
      setProgressMessage("✅ الصورة جاهزة للتحليل!");
      setUploading(false);
      
      // وقت قصير لعرض الرسالة
      await new Promise(resolve => setTimeout(resolve, 500));

      // Step 2: Analyze with VLM (without saving to DB)
      setAnalyzing(true);
      setProgress(55);
      setProgressMessage("🤖 جاري قراءة بيانات الفاتورة...");

      const analyzeResponse = await fetch(`${API_BASE}/vlm/analyze-only`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          image_url: uploadedImageUrl,
        }),
      });

      setProgress(75);
      setProgressMessage("📊 جاري استخراج المعلومات...");

      if (!analyzeResponse.ok) {
        const errorData = await analyzeResponse.json().catch(() => ({}));
        const errorMessage = errorData.detail || analyzeResponse.statusText || "فشل تحليل الفاتورة";
        console.error("Analysis error:", errorMessage);
        throw new Error(errorMessage);
      }

      const analyzeData = await analyzeResponse.json();
      setProgress(95);
      setProgressMessage("✨ تقريباً انتهينا...");
      
      await new Promise(resolve => setTimeout(resolve, 300));
      setProgress(100);
      setProgressMessage("🎉 تم بنجاح!");
      
      // ============================================================
      // ✅ Validation: تحقق إذا كانت الصورة فاتورة فعلاً
      // ============================================================
      const output = analyzeData.output || {};
      
      // ============================================================
      // ✅ Validation قوي: على الأقل 5 حقول يجب أن تكون مليئة
      // ============================================================
      const isEmpty = (val: any) => {
        if (!val) return true;
        const strVal = String(val).trim();
        return strVal === "Not Mentioned" || 
               strVal === "0" || 
               strVal === "0.00" ||
               strVal === "" ||
               strVal === "null" ||
               strVal === "undefined";
      };
      
      // عد الحقول المليئة
      const filledFields = [
        output["Vendor"],
        output["Invoice Number"],
        output["Total Amount"],
        output["Date"],
        output["Phone"],
        output["Branch"],
        output["Tax Number"],
        output["Payment Method"],
        output["Subtotal"],
        output["Tax"]
      ].filter(val => !isEmpty(val)).length;
      
      console.log("📊 Validation Check:", {
        filledFields: filledFields,
        vendor: output["Vendor"],
        total: output["Total Amount"],
        date: output["Date"],
        invoice_num: output["Invoice Number"]
      });
      
      // إذا أقل من 5 حقول مليئة = مش فاتورة!
      if (filledFields < 5) {
        throw new Error(
          "❌ عذراً، لا يمكن قراءة هذه الصورة كفاتورة!\n\n" +
          "الصورة المرفوعة لا تحتوي على معلومات كافية.\n\n" +
          "الرجاء التأكد من:\n" +
          "✓ الصورة تحتوي على فاتورة أو إيصال شراء حقيقي\n" +
          "✓ الصورة واضحة وتحتوي على:\n" +
          "  • اسم المتجر\n" +
          "  • المبلغ الإجمالي\n" +
          "  • التاريخ\n" +
          "  • رقم الفاتورة (إن وُجد)\n\n" +
          "💡 تلميح: لا يمكن رفع صور CV، مستندات نصية، أو صور شخصية."
        );
      }
      
      // Set extracted data for editing
      setExtractedData(analyzeData);
      
      // Helper لتحويل الأرقام العربية إلى إنجليزية
      const convertArabicToEnglishNumbers = (str: string): string => {
        const arabicNumbers = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
        const englishNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
        
        let result = str;
        for (let i = 0; i < arabicNumbers.length; i++) {
          result = result.replace(new RegExp(arabicNumbers[i], 'g'), englishNumbers[i]);
        }
        return result;
      };
      
      // Helper للحصول على قيمة نظيفة
      const getCleanValue = (val: any, defaultVal: string = "") => {
        if (!val || val === "Not Mentioned" || val === "null" || val === "undefined") {
          return defaultVal;
        }
        return String(val).trim();
      };
      
      // Helper للحصول على قيمة رقمية (يحول الأرقام العربية تلقائياً)
      const getNumericValue = (val: any, defaultVal: string = "0") => {
        let cleaned = getCleanValue(val, defaultVal);
        // تحويل الأرقام العربية إلى إنجليزية
        cleaned = convertArabicToEnglishNumbers(cleaned);
        // إزالة أي رموز غير رقمية (ما عدا النقطة والناقص)
        const numeric = cleaned.replace(/[^\d.-]/g, '');
        return numeric || defaultVal;
      };
      
      setEditableData({
        invoice_number: getCleanValue(analyzeData.output["Invoice Number"]),
        date: getCleanValue(analyzeData.output["Date"]),
        vendor: getCleanValue(analyzeData.output["Vendor"]),
        tax_number: getCleanValue(analyzeData.output["Tax Number"]),
        cashier: getCleanValue(analyzeData.output["Cashier"]),
        branch: getCleanValue(analyzeData.output["Branch"]),
        phone: getCleanValue(analyzeData.output["Phone"]),
        ticket_number: getCleanValue(analyzeData.output["Ticket Number"]),
        subtotal: getNumericValue(analyzeData.output["Subtotal"], "0"),
        tax: getNumericValue(analyzeData.output["Tax"], "0"),
        total_amount: getNumericValue(analyzeData.output["Total Amount"], "0"),
        grand_total: getNumericValue(analyzeData.output["Grand Total"], "0"),
        discounts: getNumericValue(analyzeData.output["Discounts"], "0"),
        amount_paid: getNumericValue(analyzeData.output["Amount Paid"], "0"),
        payment_method: getCleanValue(analyzeData.output["Payment Method"]),
        invoice_type: analyzeData.invoice_type || "فاتورة شراء",
        category: analyzeData.category || { ar: "أخرى", en: "Other" },
        ai_insight: analyzeData.ai_insight || "",
      });

      // استخراج Items من VLM response
      const extractedItems = analyzeData.output["Items"] || [];
      if (Array.isArray(extractedItems) && extractedItems.length > 0) {
        const cleanedItems = extractedItems.map((item: any) => ({
          description: getCleanValue(item.description || item.Description, ""),
          quantity: parseInt(getNumericValue(item.quantity || item.Quantity, "1")),
          unit_price: parseFloat(getNumericValue(item.unit_price || item.unit_Price || item["Unit Price"], "0")),
          total: parseFloat(getNumericValue(item.total || item.Total, "0")),
        }));
        setItems(cleanedItems);
      } else {
        // إذا لم يتم استخراج Items، نضيف item واحد فارغ
        setItems([{ description: "", quantity: 1, unit_price: 0, total: 0 }]);
      }

      toast({
        title: "تم التحليل! ✅",
        description: "راجع البيانات وعدلها إذا لزم الأمر",
      });
    } catch (error: any) {
      // Show error in a dialog (popup) instead of toast
      setErrorMessage(error.message || "حدث خطأ أثناء معالجة الفاتورة");
      setErrorDialogOpen(true);
    } finally {
      setUploading(false);
      setProcessing(false);
      setAnalyzing(false);
      setProgress(0);
      setProgressMessage("");
    }
  };

  const handleConfirmAndSave = async () => {
    if (!editableData || !imageUrl) {
      toast({
        title: "خطأ",
        description: "البيانات غير مكتملة",
        variant: "destructive",
      });
      return;
    }

    try {
      setSaving(true);

      const saveResponse = await fetch(`${API_BASE}/invoices/save-analyzed`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ...editableData,
          image_url: imageUrl,
          items: items, // إضافة Items
        }),
      });

      if (!saveResponse.ok) {
        throw new Error("فشل حفظ الفاتورة");
      }

      const savedData = await saveResponse.json();
      
      toast({
        title: "تم الحفظ! ✅",
        description: "تم حفظ الفاتورة بنجاح في قاعدة البيانات",
      });

      // Show final result
      setResult(savedData);
      setExtractedData(null);
      setEditableData(null);
    } catch (error: any) {
      toast({
        title: "خطأ ❌",
        description: error.message || "حدث خطأ أثناء حفظ الفاتورة",
        variant: "destructive",
      });
    } finally {
      setSaving(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setResult(null);
    setProgress(0);
    setExtractedData(null);
    setEditableData(null);
    setImageUrl("");
  };

  const handleEditChange = (field: string, value: string) => {
    setEditableData((prev: any) => ({
      ...prev,
      [field]: value,
    }));
  };

  // دوال Items
  const handleItemChange = (index: number, field: keyof ItemData, value: string | number) => {
    setItems((prev) => {
      const newItems = [...prev];
      newItems[index] = {
        ...newItems[index],
        [field]: value,
      };
      // حساب الـ total تلقائياً
      if (field === 'quantity' || field === 'unit_price') {
        newItems[index].total = newItems[index].quantity * newItems[index].unit_price;
      }
      return newItems;
    });
  };

  const addItem = () => {
    setItems((prev) => [...prev, { description: "", quantity: 1, unit_price: 0, total: 0 }]);
  };

  const removeItem = (index: number) => {
    setItems((prev) => prev.filter((_, i) => i !== index));
  };

  const handleCopyError = () => {
    navigator.clipboard.writeText(errorMessage);
    toast({
      title: "تم النسخ ✅",
      description: "تم نسخ رسالة الخطأ إلى الحافظة",
    });
  };

  return (
    <div className="relative min-h-screen">
      <div className="fixed inset-0 -z-10 animate-gradient opacity-90" />
      
      <main className="container mx-auto px-4 sm:px-6 md:px-16 lg:px-24 xl:px-32 py-12 sm:py-16 md:py-20 lg:py-24">
    <div className="space-y-6 sm:space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center space-y-4 sm:space-y-5 md:space-y-6 py-4 sm:py-6"
      >
        <h1 
          className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-[#8dbcc7] to-[#d4a574] px-4"
          style={{ 
            fontFamily: 'var(--font-cairo), Cairo, sans-serif',
            lineHeight: '1.5',
            paddingTop: '0.2em',
            paddingBottom: '0.2em'
          }}
        >
          رفع وتحليل الفاتورة
        </h1>
        <p className="text-base sm:text-lg md:text-xl lg:text-2xl text-gray-700 dark:text-gray-300 max-w-3xl mx-auto font-semibold px-4"
           style={{ lineHeight: '1.8' }}>
          ارفع صورة أو ملف PDF للفاتورة أو التقطها مباشرة لتحليلها
        </p>
      </motion.div>

      {/* Show editable form if data extracted */}
      {editableData && !result ? (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          dir="rtl"
        >
          <Card className="max-w-4xl mx-auto bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-0 shadow-xl rounded-2xl">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Edit2 className="w-5 h-5" />
                مراجعة وتعديل البيانات المستخرجة
              </CardTitle>
              <CardDescription>
                راجع البيانات التالية وعدلها إذا لزم الأمر، ثم اضغط &quot;تأكيد وحفظ&quot;
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Image Preview */}
              {imageUrl && (
                <div className="flex justify-center mb-4">
                  <img 
                    src={imageUrl} 
                    alt="الفاتورة" 
                    className="max-h-64 rounded-lg border-2 border-gray-200 dark:border-gray-700"
                  />
                </div>
              )}

              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <Label>رقم الفاتورة</Label>
                  <Input
                    value={editableData.invoice_number}
                    onChange={(e) => handleEditChange("invoice_number", e.target.value)}
                    placeholder="رقم الفاتورة"
                  />
                </div>
                <div>
                  <Label>التاريخ</Label>
                  <Input
                    value={editableData.date}
                    onChange={(e) => handleEditChange("date", e.target.value)}
                    placeholder="التاريخ"
                  />
                </div>
                <div>
                  <Label>اسم المتجر</Label>
                  <Input
                    value={editableData.vendor}
                    onChange={(e) => handleEditChange("vendor", e.target.value)}
                    placeholder="اسم المتجر"
                  />
                </div>
                <div>
                  <Label>نوع الفاتورة</Label>
                  <Select 
                    value={editableData.invoice_type} 
                    onValueChange={(value) => handleEditChange("invoice_type", value)}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="اختر نوع الفاتورة" />
                    </SelectTrigger>
                    <SelectContent dir="rtl">
                      <SelectItem value="فاتورة شراء">فاتورة شراء</SelectItem>
                      <SelectItem value="فاتورة ضريبية">فاتورة ضريبية</SelectItem>
                      <SelectItem value="فاتورة ضمان">فاتورة ضمان</SelectItem>
                      <SelectItem value="فاتورة صيانة">فاتورة صيانة</SelectItem>
                      <SelectItem value="إيصال">إيصال</SelectItem>
                      <SelectItem value="أخرى">أخرى</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label>الرقم الضريبي</Label>
                  <Input
                    value={editableData.tax_number}
                    onChange={(e) => handleEditChange("tax_number", e.target.value)}
                    placeholder="الرقم الضريبي"
                  />
                </div>
                <div>
                  <Label>الكاشير</Label>
                  <Input
                    value={editableData.cashier}
                    onChange={(e) => handleEditChange("cashier", e.target.value)}
                    placeholder="اسم الكاشير"
                  />
                </div>
                <div>
                  <Label>الفرع</Label>
                  <Input
                    value={editableData.branch}
                    onChange={(e) => handleEditChange("branch", e.target.value)}
                    placeholder="الفرع"
                  />
                </div>
                <div>
                  <Label>رقم الهاتف</Label>
                  <Input
                    value={editableData.phone}
                    onChange={(e) => handleEditChange("phone", e.target.value)}
                    placeholder="رقم الهاتف"
                  />
                </div>
                <div>
                  <Label>رقم التذكرة</Label>
                  <Input
                    value={editableData.ticket_number}
                    onChange={(e) => handleEditChange("ticket_number", e.target.value)}
                    placeholder="رقم التذكرة (إن وُجد)"
                  />
                </div>
                <div>
                  <Label>طريقة الدفع</Label>
                  <Input
                    value={editableData.payment_method}
                    onChange={(e) => handleEditChange("payment_method", e.target.value)}
                    placeholder="طريقة الدفع"
                  />
                </div>
              </div>

              <div className="space-y-2 pt-4 border-t">
                <h3 className="font-semibold text-lg">المبالغ المالية</h3>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <Label>المجموع الفرعي</Label>
                    <Input
                      type="number"
                      step="0.01"
                      value={editableData.subtotal}
                      onChange={(e) => handleEditChange("subtotal", e.target.value)}
                      placeholder="0.00"
                    />
                  </div>
                  <div>
                    <Label>الضريبة</Label>
                    <Input
                      type="number"
                      step="0.01"
                      value={editableData.tax}
                      onChange={(e) => handleEditChange("tax", e.target.value)}
                      placeholder="0.00"
                    />
                  </div>
                  <div>
                    <Label>الخصومات</Label>
                    <Input
                      type="number"
                      step="0.01"
                      value={editableData.discounts}
                      onChange={(e) => handleEditChange("discounts", e.target.value)}
                      placeholder="0.00"
                    />
                  </div>
                  <div>
                    <Label>المجموع الكلي (قبل الضريبة)</Label>
                    <Input
                      type="number"
                      step="0.01"
                      value={editableData.grand_total}
                      onChange={(e) => handleEditChange("grand_total", e.target.value)}
                      placeholder="0.00"
                    />
                  </div>
                  <div>
                    <Label className="font-bold">الإجمالي النهائي</Label>
                    <Input
                      type="number"
                      step="0.01"
                      value={editableData.total_amount}
                      onChange={(e) => handleEditChange("total_amount", e.target.value)}
                      placeholder="0.00"
                      className="font-bold"
                    />
                  </div>
                  <div>
                    <Label>المبلغ المدفوع</Label>
                    <Input
                      type="number"
                      step="0.01"
                      value={editableData.amount_paid}
                      onChange={(e) => handleEditChange("amount_paid", e.target.value)}
                      placeholder="0.00"
                    />
                  </div>
                </div>
              </div>
              
              {/* قسم الرؤية الذكية (Read-only) */}
              <div className="space-y-2 pt-4 border-t">
                <h3 className="font-semibold text-lg">💡 الرؤية الذكية (AI Insight)</h3>
                <div className="p-4 bg-muted/50 rounded-lg border-r-4 border-primary">
                  <p className="text-sm leading-relaxed" dir="rtl">
                    {editableData.ai_insight || "لا توجد رؤية متاحة"}
                  </p>
                </div>
                <p className="text-xs text-muted-foreground italic">
                  * هذا الحقل تم توليده تلقائياً بواسطة الذكاء الاصطناعي ولا يمكن تعديله
                </p>
              </div>

              {/* قسم العناصر (Items) */}
              <div className="space-y-3 pt-4" dir="rtl">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-bold">العناصر / المنتجات</h3>
                  <Button onClick={addItem} variant="outline" size="sm" className="gap-2">
                    <span className="text-xl">+</span> إضافة منتج
                  </Button>
                </div>

                {items.map((item, index) => (
                  <Card key={index} className="p-4">
                    <div className="grid gap-3">
                      <div className="flex justify-between items-center">
                        <span className="font-semibold">المنتج #{index + 1}</span>
                        {items.length > 1 && (
                          <Button
                            onClick={() => removeItem(index)}
                            variant="ghost"
                            size="sm"
                            className="text-red-500 hover:text-red-700"
                          >
                            حذف
                          </Button>
                        )}
                      </div>
                      
                      <div className="grid md:grid-cols-4 gap-3">
                        <div className="md:col-span-2">
                          <Label>الوصف</Label>
                          <Input
                            value={item.description}
                            onChange={(e) => handleItemChange(index, 'description', e.target.value)}
                            placeholder="مثال: قهوة أمريكية"
                          />
                        </div>
                        <div>
                          <Label>الكمية</Label>
                          <Input
                            type="number"
                            value={item.quantity}
                            onChange={(e) => handleItemChange(index, 'quantity', parseFloat(e.target.value) || 1)}
                            placeholder="1"
                          />
                        </div>
                        <div>
                          <Label>السعر</Label>
                          <Input
                            type="number"
                            step="0.01"
                            value={item.unit_price}
                            onChange={(e) => handleItemChange(index, 'unit_price', parseFloat(e.target.value) || 0)}
                            placeholder="0.00"
                          />
                        </div>
                      </div>

                      <div className="text-right">
                        <span className="text-sm text-muted-foreground">الإجمالي: </span>
                        <span className="font-bold">{item.total.toFixed(2)} ﷼</span>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>

              <div className="flex gap-3 pt-4">
                <Button
                  onClick={handleConfirmAndSave}
                  disabled={saving}
                  className="flex-1 gap-2"
                  size="lg"
                >
                  {saving ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      جاري الحفظ...
                    </>
                  ) : (
                    <>
                      <Save className="w-5 h-5" />
                      تأكيد وحفظ
                    </>
                  )}
                </Button>
                <Button
                  onClick={handleReset}
                  variant="outline"
                  className="gap-2"
                  size="lg"
                >
                  <XCircle className="w-5 h-5" />
                  إلغاء
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      ) : !result ? (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
        >
          <Card className="max-w-2xl mx-auto bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-0 shadow-xl rounded-2xl">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="w-5 h-5" />
                اختر طريقة الرفع
              </CardTitle>
              <CardDescription>
                يمكنك رفع صورة أو ملف PDF من جهازك أو التقاط صورة جديدة
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <label
                  htmlFor="file-upload"
                  className="flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-lg cursor-pointer bg-muted/50 hover:bg-muted transition-colors"
                >
                  <div className="flex flex-col items-center justify-center pt-5 pb-6">
                    <FileImage className="w-12 h-12 mb-4 text-muted-foreground" />
                    <p className="mb-2 text-sm text-muted-foreground">
                      <span className="font-semibold">انقر للرفع</span> أو اسحب الملف هنا
                    </p>
                    <p className="text-xs text-muted-foreground">PNG, JPG, JPEG, PDF (الحد الأقصى 10 ميجابايت)</p>
                  </div>
                  <input
                    id="file-upload"
                    type="file"
                    className="hidden"
                    accept="image/*,.pdf"
                    onChange={handleFileChange}
                  />
                </label>

                {file && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex items-center gap-2 p-4 rounded-lg bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800"
                  >
                    <CheckCircle className="w-5 h-5 text-green-600" />
                    <span className="text-sm font-medium">{file.name}</span>
                  </motion.div>
                )}
              </div>

              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-background px-2 text-muted-foreground">أو</span>
                </div>
              </div>

              <div className="w-full">
                <input
                  id="camera-capture"
                  type="file"
                  accept="image/*"
                  capture="environment"
                  className="hidden"
                  onChange={handleFileChange}
                />
                <label htmlFor="camera-capture" className="w-full block cursor-pointer">
                  <div className="w-full flex items-center justify-center gap-2 px-4 py-3 border-2 border-input bg-background hover:bg-accent hover:text-accent-foreground rounded-md transition-colors">
                    <Camera className="w-5 h-5" />
                    <span className="font-medium">التقاط صورة بالكاميرا</span>
                  </div>
                </label>
              </div>

              <AnimatePresence>
                {(uploading || processing || analyzing) && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 10 }}
                    className="space-y-3"
                  >
                    <div className="flex items-center justify-between text-sm">
                      <span className="font-bold text-base">
                        {progressMessage || "جاري المعالجة..."}
                      </span>
                      <span className="text-muted-foreground font-semibold">{progress}%</span>
                    </div>
                    <Progress value={progress} className="h-3" />
                    
                    {/* قائمة العمليات */}
                    <div className="space-y-2 mt-4 text-sm">
                      <div className={`flex items-center gap-2 ${progress >= 5 ? 'text-green-600 dark:text-green-400' : 'text-muted-foreground'}`}>
                        {progress >= 45 ? '✅' : progress >= 5 ? '⏳' : '⏸️'} رفع الفاتورة
                      </div>
                      <div className={`flex items-center gap-2 ${progress >= 20 ? 'text-green-600 dark:text-green-400' : 'text-muted-foreground'}`}>
                        {progress >= 45 ? '✅' : progress >= 20 ? '⏳' : '⏸️'} تحسين جودة الصورة
                      </div>
                      <div className={`flex items-center gap-2 ${progress >= 55 ? 'text-green-600 dark:text-green-400' : 'text-muted-foreground'}`}>
                        {progress >= 95 ? '✅' : progress >= 55 ? '⏳' : '⏸️'} قراءة بيانات الفاتورة
                      </div>
                      <div className={`flex items-center gap-2 ${progress >= 100 ? 'text-green-600 dark:text-green-400' : 'text-muted-foreground'}`}>
                        {progress >= 100 ? '✅' : '⏸️'} التحقق من البيانات
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              <Button
                className="w-full gap-2"
                size="lg"
                onClick={handleUpload}
                disabled={!file || uploading || processing || analyzing}
              >
                {uploading || processing || analyzing ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    جاري المعالجة...
                  </>
                ) : (
                  <>
                    <Upload className="w-5 h-5" />
                    رفع وتحليل الفاتورة
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </motion.div>
      ) : (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <InvoiceResultCard result={result} onReset={handleReset} />
        </motion.div>
      )}
    </div>
    </main>

    {/* Error Dialog - يظهر في المنتصف ويمكن نسخ النص */}
    <Dialog open={errorDialogOpen} onOpenChange={setErrorDialogOpen}>
      <DialogContent className="sm:max-w-[500px] max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-destructive text-xl">
            <XCircle className="w-6 h-6" />
            خطأ في معالجة الفاتورة
          </DialogTitle>
        </DialogHeader>
        
        <div className="py-4">
          <div className="bg-destructive/10 border border-destructive/30 rounded-lg p-4 text-right">
            <pre className="whitespace-pre-wrap text-sm leading-relaxed font-medium text-foreground select-all">
              {errorMessage}
            </pre>
          </div>
        </div>

        <DialogFooter className="flex-row gap-2 sm:gap-3">
          <Button
            variant="outline"
            onClick={handleCopyError}
            className="gap-2 flex-1"
          >
            <Copy className="w-4 h-4" />
            نسخ النص
          </Button>
          <Button
            onClick={() => setErrorDialogOpen(false)}
            className="flex-1"
          >
            حسناً
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
    </div>
  );
}
