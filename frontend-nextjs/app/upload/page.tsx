"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Upload, Camera, FileImage, CheckCircle, XCircle, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { useToast } from "@/components/ui/use-toast";
import { API_BASE } from "@/lib/utils";
import InvoiceResultCard from "@/components/InvoiceResultCard";
import CameraCapture from "@/components/CameraCapture";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState<any>(null);
  const [showCamera, setShowCamera] = useState(false);
  const { toast } = useToast();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setResult(null);
    }
  };

  const handleCameraCapture = (capturedFile: File) => {
    setFile(capturedFile);
    setShowCamera(false);
    setResult(null);
  };

  const handleUpload = async () => {
    if (!file) {
      toast({
        title: "خطأ",
        description: "الرجاء اختيار صورة فاتورة أولاً",
        variant: "destructive",
      });
      return;
    }

    try {
      // Step 1: Upload to Supabase
      setUploading(true);
      setProgress(10);

      const formData = new FormData();
      formData.append("file", file);

      const uploadResponse = await fetch(`${API_BASE}/upload/`, {
        method: "POST",
        body: formData,
      });

      if (!uploadResponse.ok) {
        throw new Error("فشل رفع الصورة");
      }

      const uploadData = await uploadResponse.json();
      const imageUrl = uploadData.url;

      setProgress(40);
      setUploading(false);

      // Step 2: Analyze with VLM
      setAnalyzing(true);
      setProgress(60);

      const analyzeResponse = await fetch(`${API_BASE}/vlm/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          image_url: imageUrl,
        }),
      });

      if (!analyzeResponse.ok) {
        throw new Error("فشل تحليل الفاتورة");
      }

      const analyzeData = await analyzeResponse.json();
      setProgress(100);
      setResult(analyzeData);

      toast({
        title: "نجح! ✅",
        description: "تم تحليل الفاتورة بنجاح",
      });
    } catch (error: any) {
      toast({
        title: "خطأ ❌",
        description: error.message || "حدث خطأ أثناء معالجة الفاتورة",
        variant: "destructive",
      });
    } finally {
      setUploading(false);
      setAnalyzing(false);
      setProgress(0);
    }
  };

  const handleReset = () => {
    setFile(null);
    setResult(null);
    setProgress(0);
  };

  return (
    <div className="relative min-h-screen">
      {/* Fixed Animated Background */}
      <div className="fixed inset-0 -z-10 animate-gradient opacity-90" />
      
      <main className="container mx-auto px-6 md:px-16 lg:px-24 xl:px-32 py-20 md:py-24">
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center space-y-4"
      >
        <h1 className="text-5xl md:text-6xl font-black bg-gradient-to-l from-[#8dbcc7] to-[#d4a574] bg-clip-text text-transparent">
          رفع وتحليل الفاتورة
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-400">
          ارفع صورة الفاتورة أو التقطها مباشرة لتحليلها بالذكاء الاصطناعي
        </p>
      </motion.div>

      {!result ? (
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
                يمكنك رفع صورة من جهازك أو التقاط صورة جديدة
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* File Upload */}
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
                    <p className="text-xs text-muted-foreground">PNG, JPG, JPEG (الحد الأقصى 10 ميجابايت)</p>
                  </div>
                  <input
                    id="file-upload"
                    type="file"
                    className="hidden"
                    accept="image/*"
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

              {/* Camera Button */}
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-background px-2 text-muted-foreground">أو</span>
                </div>
              </div>

              <Button
                variant="outline"
                className="w-full gap-2"
                onClick={() => setShowCamera(!showCamera)}
              >
                <Camera className="w-5 h-5" />
                {showCamera ? "إخفاء الكاميرا" : "التقاط صورة بالكاميرا"}
              </Button>

              {showCamera && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                >
                  <CameraCapture onCapture={handleCameraCapture} />
                </motion.div>
              )}

              {/* Upload Progress */}
              <AnimatePresence>
                {(uploading || analyzing) && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 10 }}
                    className="space-y-2"
                  >
                    <div className="flex items-center justify-between text-sm">
                      <span className="font-medium">
                        {uploading ? "جاري رفع الصورة..." : "جاري التحليل..."}
                      </span>
                      <span className="text-muted-foreground">{progress}%</span>
                    </div>
                    <Progress value={progress} />
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Submit Button */}
              <Button
                className="w-full gap-2"
                size="lg"
                onClick={handleUpload}
                disabled={!file || uploading || analyzing}
              >
                {uploading || analyzing ? (
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

