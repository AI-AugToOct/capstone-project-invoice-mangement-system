"use client";

import { Dialog, DialogContent } from "@/components/ui/dialog";
import { X, Download, ZoomIn, ZoomOut } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState } from "react";

interface ImageModalProps {
  imageUrl: string | null;
  onClose: () => void;
  title?: string;
}

export default function ImageModal({ imageUrl, onClose, title }: ImageModalProps) {
  const [zoom, setZoom] = useState(1);

  const handleDownload = () => {
    if (!imageUrl) return;
    
    const link = document.createElement('a');
    link.href = imageUrl;
    link.download = `invoice-${Date.now()}.jpg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <Dialog open={!!imageUrl} onOpenChange={onClose}>
      <DialogContent className="max-w-5xl p-0 overflow-hidden" dir="rtl">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b bg-background/95 backdrop-blur">
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setZoom(Math.max(0.5, zoom - 0.25))}
              disabled={zoom <= 0.5}
            >
              <ZoomOut className="w-4 h-4" />
            </Button>
            <span className="text-sm font-medium">{Math.round(zoom * 100)}%</span>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setZoom(Math.min(3, zoom + 0.25))}
              disabled={zoom >= 3}
            >
              <ZoomIn className="w-4 h-4" />
            </Button>
          </div>

          <h3 className="text-lg font-semibold">{title || "معاينة الفاتورة"}</h3>

          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="icon"
              onClick={handleDownload}
              className="hover:bg-green-100 dark:hover:bg-green-950"
            >
              <Download className="w-4 h-4" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={onClose}
              className="hover:bg-red-100 dark:hover:bg-red-950"
            >
              <X className="w-4 h-4" />
            </Button>
          </div>
        </div>

        {/* Image */}
        <div className="relative w-full h-[70vh] overflow-auto bg-muted/20 flex items-center justify-center p-4">
          {imageUrl && (
            <img
              src={imageUrl}
              alt={title || "فاتورة"}
              className="rounded-lg shadow-2xl transition-transform duration-300"
              style={{ 
                transform: `scale(${zoom})`,
                maxWidth: '100%',
                height: 'auto'
              }}
              onError={(e) => {
                const target = e.target as HTMLImageElement;
                target.src = '/placeholder-invoice.png';
              }}
            />
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}

