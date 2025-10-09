"use client";

import { useRef, useState, useEffect } from "react";
import { Camera, XCircle } from "lucide-react";
import { Button } from "./ui/button";
import { Card } from "./ui/card";

interface CameraCaptureProps {
  onCapture: (file: File) => void;
}

export default function CameraCapture({ onCapture }: CameraCaptureProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    startCamera();
    return () => {
      stopCamera();
    };
  }, []);

  const startCamera = async () => {
    try {
      // Enhanced constraints for better mobile support
      const constraints = {
        video: {
          facingMode: "environment", // Use back camera on mobile
          width: { ideal: 1920, max: 1920 },
          height: { ideal: 1080, max: 1080 },
        },
        audio: false,
      };
      
      const mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
      setStream(mediaStream);
      
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
        // Ensure video plays on iOS Safari
        videoRef.current.setAttribute('playsinline', '');
        videoRef.current.play().catch(err => {
          console.error("Video play error:", err);
          setError("فشل تشغيل الكاميرا. حاول مرة أخرى.");
        });
      }
    } catch (err: any) {
      console.error("Camera error:", err);
      if (err.name === 'NotAllowedError') {
        setError("الرجاء السماح بالوصول إلى الكاميرا من إعدادات المتصفح.");
      } else if (err.name === 'NotFoundError') {
        setError("لم يتم العثور على كاميرا. تأكد من وجود كاميرا متصلة.");
      } else {
        setError("فشل الوصول إلى الكاميرا. الرجاء المحاولة مرة أخرى.");
      }
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
    }
  };

  const capturePhoto = () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");

    if (!context) return;

    // Set canvas dimensions to video dimensions
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw video frame to canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert canvas to blob then file
    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], `invoice-${Date.now()}.jpg`, {
          type: "image/jpeg",
        });
        onCapture(file);
        stopCamera();
      }
    }, "image/jpeg", 0.9);
  };

  if (error) {
    return (
      <Card className="p-6 border-destructive bg-destructive/10">
        <div className="flex items-center gap-2 text-destructive">
          <XCircle className="w-5 h-5" />
          <p>{error}</p>
        </div>
      </Card>
    );
  }

  return (
    <Card className="overflow-hidden">
      <div className="relative bg-black">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="w-full h-auto max-h-[60vh] object-cover rounded-t-lg"
          style={{ minHeight: '300px' }}
        />
        <canvas ref={canvasRef} className="hidden" />
        <div className="p-4 bg-background">
          <Button onClick={capturePhoto} className="w-full gap-2" size="lg">
            <Camera className="w-5 h-5" />
            التقاط الصورة
          </Button>
        </div>
      </div>
    </Card>
  );
}

