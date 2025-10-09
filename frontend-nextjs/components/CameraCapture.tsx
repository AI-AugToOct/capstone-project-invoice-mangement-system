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
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    startCamera();
    return () => {
      stopCamera();
    };
  }, []);

  const startCamera = async () => {
    try {
      setLoading(true);
      
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
        
        // Wait for video to load before playing
        videoRef.current.onloadedmetadata = () => {
          if (videoRef.current) {
            videoRef.current.play()
              .then(() => {
                setLoading(false);
              })
              .catch(err => {
                console.error("Video play error:", err);
                setError("فشل تشغيل الكاميرا. حاول مرة أخرى.");
                setLoading(false);
              });
          }
        };
      }
    } catch (err: any) {
      console.error("Camera error:", err);
      setLoading(false);
      
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
      <div className="relative bg-black aspect-video">
        {loading && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-900">
            <div className="text-center">
              <div className="w-12 h-12 border-4 border-[#8dbcc7] border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
              <p className="text-white text-sm">جاري تحميل الكاميرا...</p>
            </div>
          </div>
        )}
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className={`w-full h-full object-cover rounded-t-lg ${loading ? 'opacity-0' : 'opacity-100'} transition-opacity duration-300`}
        />
        <canvas ref={canvasRef} className="hidden" />
        <div className="p-4 bg-background">
          <Button 
            onClick={capturePhoto} 
            className="w-full gap-2" 
            size="lg"
            disabled={loading}
          >
            <Camera className="w-5 h-5" />
            التقاط الصورة
          </Button>
        </div>
      </div>
    </Card>
  );
}

