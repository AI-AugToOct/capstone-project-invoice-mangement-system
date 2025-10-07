"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, MessageSquare, Bot, User, Loader2, Sparkles, Store, Calendar, DollarSign, Download, Eye } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useToast } from "@/components/ui/use-toast";
import { API_BASE } from "@/lib/utils";
import Image from "next/image";
import ImageModal from "@/components/ImageModal";
import { downloadInvoiceAsPDF } from "@/lib/pdfUtils";
import GlobalLoader from "@/components/GlobalLoader";

interface Invoice {
  id: number;
  vendor: string;
  invoice_number?: string;
  invoice_type?: string;
  date: string;
  total: string;
  tax?: string;
  payment_method?: string;
  image_url?: string;
  category?: string;
}

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  invoices?: Invoice[];
  timestamp: Date;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content: "مرحبًا! أنا مساعدك الذكي لتحليل الفواتير. اسألني أي سؤال عن فواتيرك مثل:\n\n• ما هو إجمالي مصروفاتي هذا الشهر؟\n• ما أكثر متجر أشتري منه؟\n• كم فاتورة لدي من المطاعم؟",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [pdfLoading, setPdfLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE}/chat/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: userMessage.content,
        }),
      });

      if (!response.ok) {
        throw new Error("فشل الحصول على الإجابة");
      }

      const data = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.answer || "عذرًا، لم أتمكن من الحصول على إجابة.",
        invoices: data.invoices || undefined,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error: any) {
      toast({
        title: "خطأ",
        description: error.message || "حدث خطأ أثناء معالجة السؤال",
        variant: "destructive",
      });

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "عذرًا، حدث خطأ أثناء معالجة سؤالك. الرجاء المحاولة مرة أخرى.",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const suggestedQuestions = [
    "ما هو إجمالي مصروفاتي؟",
    "ما أكثر متجر أشتري منه؟",
    "كم فاتورة لدي من المطاعم؟",
    "ما هو متوسط قيمة فواتيري؟",
  ];

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
        className="text-center space-y-4"
      >
        <h1 className="text-5xl md:text-6xl font-black bg-gradient-to-l from-[#8dbcc7] to-[#d4a574] bg-clip-text text-transparent">
          الدردشة الذكية
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-400">
          اسأل أي سؤال عن فواتيرك واحصل على إجابات فورية
        </p>
      </motion.div>

      {/* Chat Container */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.1 }}
        className="max-w-4xl mx-auto"
      >
        <Card className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-0 shadow-xl rounded-2xl">
          <CardHeader className="border-b bg-muted/50">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div>
                <CardTitle>مساعد مُفَوْتِر الذكي</CardTitle>
                <CardDescription>متصل ونشط</CardDescription>
              </div>
            </div>
          </CardHeader>

          <CardContent className="p-0">
            {/* Messages Area */}
            <ScrollArea className="h-[500px] p-6" ref={scrollRef}>
              <div className="space-y-4">
                <AnimatePresence>
                  {messages.map((message, index) => (
                    <motion.div
                      key={message.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ duration: 0.3 }}
                      className={`flex gap-3 ${
                        message.role === "user" ? "flex-row-reverse" : "flex-row"
                      }`}
                    >
                      {/* Avatar */}
                      <div
                        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                          message.role === "user"
                            ? "bg-gradient-to-br from-blue-500 to-cyan-500"
                            : "bg-gradient-to-br from-purple-500 to-pink-500"
                        }`}
                      >
                        {message.role === "user" ? (
                          <User className="w-4 h-4 text-white" />
                        ) : (
                          <Bot className="w-4 h-4 text-white" />
                        )}
                      </div>

                      {/* Message Bubble */}
                      <div
                        className={`flex-1 max-w-[80%] ${
                          message.role === "user" ? "text-left" : "text-right"
                        }`}
                      >
                        <div
                          className={`inline-block p-4 rounded-2xl ${
                            message.role === "user"
                              ? "bg-primary text-primary-foreground rounded-br-sm"
                              : "bg-muted rounded-bl-sm"
                          }`}
                        >
                          <p className="text-sm leading-relaxed whitespace-pre-wrap">
                            {message.content}
                          </p>
                        </div>
                        
                        {/* عرض الفواتير إذا كانت موجودة */}
                        {message.invoices && message.invoices.length > 0 && (
                          <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.2 }}
                            className={`mt-3 ${message.invoices.length > 1 ? 'grid grid-cols-1 md:grid-cols-2 gap-2' : 'space-y-2'}`}
                          >
                            {message.invoices.map((invoice, idx) => (
                              <motion.div
                                key={invoice.id}
                                initial={{ opacity: 0, scale: 0.95 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ delay: 0.2 + idx * 0.1 }}
                              >
                                <Card className="overflow-hidden hover:shadow-xl transition-all duration-300 hover:scale-105 border-r-4 border-r-blue-500">
                                  {/* صورة الفاتورة */}
                                  <div className="relative w-full h-48 bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-800 dark:to-gray-900 overflow-hidden cursor-pointer group"
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
                                            target.onerror = null;
                                          }}
                                        />
                                        {/* Gradient overlay */}
                                        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                                        
                                        {/* Hover Eye Icon */}
                                        <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black/20">
                                          <div className="bg-white/90 dark:bg-black/80 rounded-full p-3 backdrop-blur-sm">
                                            <Eye className="w-6 h-6" />
                                          </div>
                                        </div>
                                        
                                        {/* Invoice number badge */}
                                        {invoice.invoice_number && (
                                          <div className="absolute top-2 left-2 px-2 py-1 rounded-md bg-white/90 dark:bg-black/80 text-xs font-medium backdrop-blur-sm" dir="ltr">
                                            #{invoice.invoice_number}
                                          </div>
                                        )}
                                        
                                        {/* Invoice type badge */}
                                        {invoice.invoice_type && invoice.invoice_type !== "غير محدد" && (
                                          <div className="absolute top-2 right-2 px-2 py-1 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 text-white text-xs font-bold shadow-lg" dir="rtl">
                                            {invoice.invoice_type}
                                          </div>
                                        )}
                                      </>
                                    ) : (
                                      <div className="flex items-center justify-center h-full">
                                        <div className="text-center text-gray-400">
                                          <Store className="w-12 h-12 mx-auto mb-2" />
                                          <p className="text-xs">لا توجد صورة</p>
                                        </div>
                                      </div>
                                    )}
                                  </div>
                                  
                                  {/* معلومات الفاتورة */}
                                  <div className="p-3 space-y-2" dir="rtl">
                                    {/* اسم المتجر */}
                                    <div className="flex items-center gap-2">
                                      <Store className="w-4 h-4 text-blue-600 flex-shrink-0" />
                                      <p className="text-sm font-bold truncate">
                                        {invoice.vendor || "متجر غير معروف"}
                                      </p>
                                    </div>
                                    
                                    {/* نوع الفاتورة */}
                                    {invoice.invoice_type && invoice.invoice_type !== "غير محدد" && (
                                      <div className="text-xs text-muted-foreground flex items-center gap-1">
                                        <span className="w-2 h-2 bg-purple-500 rounded-full" />
                                        نوع الفاتورة: {invoice.invoice_type}
                                      </div>
                                    )}
                                    
                                    {/* التاريخ */}
                                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                                      <Calendar className="w-3 h-3 flex-shrink-0" />
                                      <span>
                                        {invoice.date
                                          ? new Date(invoice.date).toLocaleDateString("ar-SA", {
                                              year: "numeric",
                                              month: "long",
                                              day: "numeric"
                                            })
                                          : "تاريخ غير محدد"}
                                      </span>
                                    </div>
                                    
                                    {/* المبلغ والضريبة */}
                                    <div className="flex items-center justify-between pt-2 border-t">
                                      <div className="flex items-center gap-1">
                                        <DollarSign className="w-4 h-4 text-green-600" />
                                        <span className="text-base font-bold text-green-600">
                                          {parseFloat(invoice.total || "0").toFixed(2)} ر.س
                                        </span>
                                      </div>
                                      
                                      {invoice.tax && parseFloat(invoice.tax) > 0 && (
                                        <span className="text-xs text-muted-foreground">
                                          ضريبة: {parseFloat(invoice.tax).toFixed(2)} ر.س
                                        </span>
                                      )}
                                    </div>
                                    
                                    {/* طريقة الدفع */}
                                    {invoice.payment_method && invoice.payment_method !== "غير محدد" && (
                                      <div className="text-xs text-muted-foreground flex items-center gap-1">
                                        <span className="w-2 h-2 bg-blue-500 rounded-full" />
                                        {invoice.payment_method}
                                      </div>
                                    )}
                                    
                                    {/* PDF Download Button */}
                                    <Button
                                      onClick={async (e) => {
                                        e.stopPropagation();
                                        try {
                                          setPdfLoading(true);
                                          await downloadInvoiceAsPDF(invoice);
                                          toast({
                                            title: "تم التنزيل",
                                            description: "تم تنزيل الفاتورة بنجاح",
                                          });
                                        } catch (error) {
                                          toast({
                                            title: "خطأ",
                                            description: "فشل تنزيل الفاتورة",
                                            variant: "destructive",
                                          });
                                        } finally {
                                          setPdfLoading(false);
                                        }
                                      }}
                                      disabled={pdfLoading}
                                      variant="outline"
                                      size="sm"
                                      className="w-full mt-2"
                                    >
                                      <Download className="w-3 h-3 ml-1" />
                                      {pdfLoading ? "جاري..." : "تحميل PDF"}
                                    </Button>
                                  </div>
                                </Card>
                              </motion.div>
                            ))}
                          </motion.div>
                        )}
                        
                        <p className="text-xs text-muted-foreground mt-1 px-2">
                          {message.timestamp.toLocaleTimeString("ar-SA", {
                            hour: "2-digit",
                            minute: "2-digit",
                          })}
                        </p>
                      </div>
                    </motion.div>
                  ))}
                </AnimatePresence>

                {/* Typing Indicator */}
                {loading && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex gap-3"
                  >
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                      <Bot className="w-4 h-4 text-white" />
                    </div>
                    <div className="bg-muted p-4 rounded-2xl rounded-bl-sm">
                      <div className="flex gap-1">
                        <div className="w-2 h-2 rounded-full bg-muted-foreground animate-typing" />
                        <div
                          className="w-2 h-2 rounded-full bg-muted-foreground animate-typing"
                          style={{ animationDelay: "0.2s" }}
                        />
                        <div
                          className="w-2 h-2 rounded-full bg-muted-foreground animate-typing"
                          style={{ animationDelay: "0.4s" }}
                        />
                      </div>
                    </div>
                  </motion.div>
                )}
              </div>
            </ScrollArea>

            {/* Suggested Questions */}
            {messages.length === 1 && (
              <div className="px-6 pb-4 border-t pt-4">
                <p className="text-sm font-medium mb-3">أسئلة مقترحة:</p>
                <div className="flex flex-wrap gap-2">
                  {suggestedQuestions.map((question) => (
                    <Button
                      key={question}
                      variant="outline"
                      size="sm"
                      onClick={() => setInput(question)}
                      className="text-xs"
                    >
                      {question}
                    </Button>
                  ))}
                </div>
              </div>
            )}

            {/* Input Area */}
            <div className="p-4 border-t bg-muted/30">
              <div className="flex gap-2">
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="اكتب سؤالك هنا..."
                  className="flex-1 min-h-[60px] max-h-[120px] p-3 rounded-lg border bg-background resize-none focus:outline-none focus:ring-2 focus:ring-ring"
                  disabled={loading}
                />
                <Button
                  onClick={handleSend}
                  disabled={!input.trim() || loading}
                  size="lg"
                  className="self-end gap-2"
                >
                  {loading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <>
                      <Send className="w-5 h-5" />
                      إرسال
                    </>
                  )}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Tips Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="max-w-4xl mx-auto"
      >
        <Card className="border-2 border-blue-200 dark:border-blue-800 bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-950 dark:to-cyan-950">
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <MessageSquare className="w-5 h-5 text-blue-600" />
              نصائح للاستخدام
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li className="flex items-start gap-2">
                <span>•</span>
                <span>اسأل عن إجمالي المصروفات أو متوسط الفواتير</span>
              </li>
              <li className="flex items-start gap-2">
                <span>•</span>
                <span>استفسر عن فواتير متجر معين أو فئة معينة</span>
              </li>
              <li className="flex items-start gap-2">
                <span>•</span>
                <span>احصل على تحليلات ذكية عن عادات الإنفاق</span>
              </li>
            </ul>
          </CardContent>
        </Card>
      </motion.div>

      {/* Image Modal */}
      <ImageModal
        imageUrl={selectedImage}
        onClose={() => setSelectedImage(null)}
        title="معاينة الفاتورة"
      />

      {/* Global Loader */}
      <GlobalLoader show={loading} message="جاري معالجة سؤالك..." />
    </div>
    </main>
    </div>
  );
}


