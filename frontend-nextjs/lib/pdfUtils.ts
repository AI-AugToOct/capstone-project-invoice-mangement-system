import { jsPDF } from 'jspdf';

interface Invoice {
  id: number;
  vendor: string;
  invoice_number?: string;
  invoice_type?: string;
  invoice_date: string;
  total_amount: string;
  tax?: string;
  payment_method?: string;
  image_url?: string;
}

/**
 * Downloads the actual invoice image as PDF
 * Uses the original uploaded image from Supabase Storage
 */
export async function downloadInvoiceAsPDF(invoice: Invoice) {
  if (!invoice?.image_url) {
    alert("❌ لا توجد صورة متوفرة لهذه الفاتورة.");
    throw new Error("No image URL available");
  }

  try {
    // Fetch the actual invoice image from Supabase
    const response = await fetch(invoice.image_url);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch image: ${response.statusText}`);
    }
    
    const blob = await response.blob();
    const reader = new FileReader();

    return new Promise<void>((resolve, reject) => {
      reader.onloadend = () => {
        try {
          const imgData = reader.result as string;
          
          // Create PDF with A4 portrait orientation
          const pdf = new jsPDF({
            orientation: "portrait",
            unit: "px",
            format: "a4",
          });

          const pageWidth = pdf.internal.pageSize.getWidth();
          const pageHeight = pdf.internal.pageSize.getHeight();

          // Add the original invoice image to PDF (preserves quality and layout)
          pdf.addImage(imgData, "JPEG", 0, 0, pageWidth, pageHeight);
          
          // Download with vendor name
          const filename = `${invoice.vendor || "فاتورة"}_${invoice.invoice_number || invoice.id}.pdf`;
          pdf.save(filename);
          
          resolve();
        } catch (error) {
          reject(error);
        }
      };

      reader.onerror = () => {
        reject(new Error("Failed to read image data"));
      };

      reader.readAsDataURL(blob);
    });
  } catch (error) {
    console.error("PDF Download Error:", error);
    alert("حدث خطأ أثناء تحميل الصورة.");
    throw error;
  }
}


