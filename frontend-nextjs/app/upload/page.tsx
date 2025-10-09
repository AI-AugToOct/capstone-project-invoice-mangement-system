"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Upload, Camera, FileImage, CheckCircle, XCircle, Loader2, Save, Edit2 } from "lucide-react";
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
  const [result, setResult] = useState<any>(null);
  const [imageUrl, setImageUrl] = useState<string>("");
  const { toast } = useToast();
  const { theme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

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
      setProgressMessage("📤 جاري رفع الصورة...");

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
      setProgressMessage("🔧 جاري معالجة الصورة وتصحيحها...");
      
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
      setProgressMessage("✅ تم تصحيح الصورة بنجاح!");
      setUploading(false);
      
      // وقت قصير لعرض الرسالة
      await new Promise(resolve => setTimeout(resolve, 500));

      // Step 2: Analyze with VLM (without saving to DB)
      setAnalyzing(true);
      setProgress(55);
      setProgressMessage("🤖 جاري تحليل الفاتورة بالذكاء الاصطناعي...");

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
      setProgressMessage("📊 جاري استخراج البيانات...");

      if (!analyzeResponse.ok) {
        const errorData = await analyzeResponse.json().catch(() => ({}));
        const errorMessage = errorData.detail || analyzeResponse.statusText || "فشل تحليل الفاتورة";
        console.error("Analysis error:", errorMessage);
        throw new Error(errorMessage);
      }

      const analyzeData = await analyzeResponse.json();
      setProgress(95);
      setProgressMessage("✨ جاري تجهيز النتائج...");
      
      await new Promise(resolve => setTimeout(resolve, 300));
      setProgress(100);
      setProgressMessage("🎉 تم بنجاح!");
      
      // Set extracted data for editing
      setExtractedData(analyzeData);
      setEditableData({
        invoice_number: analyzeData.output["Invoice Number"] || "",
        date: analyzeData.output["Date"] || "",
        vendor: analyzeData.output["Vendor"] || "",
        tax_number: analyzeData.output["Tax Number"] || "",
        cashier: analyzeData.output["Cashier"] || "",
        branch: analyzeData.output["Branch"] || "",
        phone: analyzeData.output["Phone"] || "",
        subtotal: analyzeData.output["Subtotal"] || "0",
        tax: analyzeData.output["Tax"] || "0",
        total_amount: analyzeData.output["Total Amount"] || "0",
        discounts: analyzeData.output["Discounts"] || "0",
        payment_method: analyzeData.output["Payment Method"] || "",
        invoice_type: analyzeData.invoice_type || "فاتورة شراء",
        category: analyzeData.category || { ar: "أخرى", en: "Other" },
        ai_insight: analyzeData.ai_insight || "",
      });

      toast({
        title: "تم التحليل! ✅",
        description: "راجع البيانات وعدلها إذا لزم الأمر",
      });
    } catch (error: any) {
      toast({
        title: "خطأ ❌",
        description: error.message || "حدث خطأ أثناء معالجة الفاتورة",
        variant: "destructive",
      });
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
                </div>
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
                        {progress >= 45 ? '✅' : progress >= 5 ? '⏳' : '⏸️'} رفع الصورة
                      </div>
                      <div className={`flex items-center gap-2 ${progress >= 20 ? 'text-green-600 dark:text-green-400' : 'text-muted-foreground'}`}>
                        {progress >= 45 ? '✅' : progress >= 20 ? '⏳' : '⏸️'} تصحيح الدوران والميل (OpenCV)
                      </div>
                      <div className={`flex items-center gap-2 ${progress >= 55 ? 'text-green-600 dark:text-green-400' : 'text-muted-foreground'}`}>
                        {progress >= 95 ? '✅' : progress >= 55 ? '⏳' : '⏸️'} تحليل البيانات بالذكاء الاصطناعي
                      </div>
                      <div className={`flex items-center gap-2 ${progress >= 100 ? 'text-green-600 dark:text-green-400' : 'text-muted-foreground'}`}>
                        {progress >= 100 ? '✅' : '⏸️'} تجهيز النتائج
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
    </div>
  );
}
