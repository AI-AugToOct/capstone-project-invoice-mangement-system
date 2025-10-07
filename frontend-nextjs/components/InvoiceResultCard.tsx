"use client";

import { motion } from "framer-motion";
import {
  FileText,
  Calendar,
  DollarSign,
  Store,
  Tag,
  Receipt,
  Phone,
  MapPin,
  CreditCard,
  Sparkles,
  RotateCcw,
} from "lucide-react";
import { Button } from "./ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";

interface InvoiceResultCardProps {
  result: any;
  onReset: () => void;
}

export default function InvoiceResultCard({ result, onReset }: InvoiceResultCardProps) {
  const output = result.output || {};
  const category = result.category || { ar: "غير محدد", en: "Other" };
  const aiInsight = result.ai_insight || "لا توجد رؤى متاحة";
  const invoiceType = result.invoice_type || output["Invoice_Type"] || "فاتورة شراء";

  const infoItems = [
    {
      icon: Receipt,
      label: "رقم الفاتورة",
      value: output["Invoice Number"] || "غير متوفر",
      color: "text-blue-600",
    },
    {
      icon: Calendar,
      label: "التاريخ",
      value: output["Date"] || "غير متوفر",
      color: "text-purple-600",
    },
    {
      icon: Store,
      label: "المتجر",
      value: output["Vendor"] || "غير متوفر",
      color: "text-green-600",
    },
    {
      icon: MapPin,
      label: "الفرع",
      value: output["Branch"] || "غير متوفر",
      color: "text-orange-600",
    },
    {
      icon: Phone,
      label: "الهاتف",
      value: output["Phone"] || "غير متوفر",
      color: "text-pink-600",
    },
    {
      icon: CreditCard,
      label: "طريقة الدفع",
      value: output["Payment Method"] || "غير متوفر",
      color: "text-indigo-600",
    },
  ];

  const financialItems = [
    {
      label: "المجموع الفرعي",
      value: output["Subtotal"],
      icon: "💰",
    },
    {
      label: "الضريبة",
      value: output["Tax"],
      icon: "📊",
    },
    {
      label: "الخصومات",
      value: output["Discounts"] || "0.00",
      icon: "🎁",
    },
    {
      label: "الإجمالي النهائي",
      value: output["Total Amount"],
      icon: "💵",
      highlight: true,
    },
  ];

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Success Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center space-y-2"
      >
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-green-100 dark:bg-green-950 text-green-700 dark:text-green-300">
          <Sparkles className="w-4 h-4" />
          <span className="font-medium">تم التحليل بنجاح!</span>
        </div>
      </motion.div>

      {/* Category & Invoice Type Cards */}
      <div className="grid md:grid-cols-2 gap-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
        >
          <Card className="border-2 border-[#8dbcc7]/20 bg-gradient-to-br from-[#8dbcc7]/5 to-[#d4a574]/5">
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-[#8dbcc7] to-[#6fa3b0] flex items-center justify-center shadow-lg">
                  <Tag className="w-6 h-6 text-white" />
                </div>
                <div>
                  <CardTitle className="text-sm text-muted-foreground">تصنيف النشاط التجاري</CardTitle>
                  <CardDescription className="text-xl font-black text-foreground mt-1">
                    {category.ar}
                  </CardDescription>
                </div>
              </div>
            </CardHeader>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.15 }}
        >
          <Card className="border-2 border-[#d4a574]/20 bg-gradient-to-br from-[#d4a574]/5 to-[#8dbcc7]/5">
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-[#d4a574] to-[#c89563] flex items-center justify-center shadow-lg">
                  <FileText className="w-6 h-6 text-white" />
                </div>
                <div>
                  <CardTitle className="text-sm text-muted-foreground">نوع الفاتورة</CardTitle>
                  <CardDescription className="text-xl font-black text-foreground mt-1">
                    {invoiceType}
                  </CardDescription>
                </div>
              </div>
            </CardHeader>
          </Card>
        </motion.div>
      </div>

      {/* Invoice Details Grid */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="grid md:grid-cols-2 gap-4"
      >
        {infoItems.map((item, index) => (
          <motion.div
            key={item.label}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 + index * 0.05 }}
          >
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-start gap-3">
                  <item.icon className={`w-5 h-5 mt-0.5 ${item.color}`} />
                  <div className="flex-1">
                    <p className="text-sm text-muted-foreground">{item.label}</p>
                    <p className="font-semibold mt-1">{item.value}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </motion.div>

      {/* Financial Summary */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <Card className="border-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <DollarSign className="w-5 h-5" />
              الملخص المالي
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {financialItems.map((item, index) => (
              <div
                key={item.label}
                className={`flex items-center justify-between p-3 rounded-lg ${
                  item.highlight
                    ? "bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-950 dark:to-emerald-950 border-2 border-green-200 dark:border-green-800"
                    : "bg-muted/50"
                }`}
              >
                <div className="flex items-center gap-2">
                  <span className="text-xl">{item.icon}</span>
                  <span className={item.highlight ? "font-bold text-lg" : "font-medium"}>
                    {item.label}
                  </span>
                </div>
                <span className={item.highlight ? "font-bold text-xl text-green-600" : "font-semibold"}>
                  {item.value} ر.س
                </span>
              </div>
            ))}
          </CardContent>
        </Card>
      </motion.div>

      {/* AI Insight */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <Card className="border-2 border-purple-200 dark:border-purple-800 bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-950 dark:to-pink-950">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-purple-600" />
              رؤية ذكية من الذكاء الاصطناعي
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground leading-relaxed">{aiInsight}</p>
          </CardContent>
        </Card>
      </motion.div>

      {/* Items List */}
      {output.Items && output.Items.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="w-5 h-5" />
                تفاصيل المشتريات
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {output.Items.map((item: any, index: number) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-3 rounded-lg bg-muted/50 hover:bg-muted transition-colors"
                  >
                    <div className="flex-1">
                      <p className="font-medium">{item.description || "عنصر غير معروف"}</p>
                      <p className="text-sm text-muted-foreground">
                        الكمية: {item.quantity || 1} × {item.unit_price || 0} ر.س
                      </p>
                    </div>
                    <p className="font-semibold">{item.total || 0} ر.س</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* Reset Button */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.7 }}
        className="text-center"
      >
        <Button onClick={onReset} variant="outline" size="lg" className="gap-2">
          <RotateCcw className="w-5 h-5" />
          رفع فاتورة جديدة
        </Button>
      </motion.div>
    </div>
  );
}

