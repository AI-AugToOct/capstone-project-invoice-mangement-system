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
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment" }, // Use back camera on mobile
        audio: false,
      });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (err: any) {
      setError("فشل الوصول إلى الكاميرا. الرجاء التحقق من الأذونات.");
      console.error("Camera error:", err);
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
      <div className="relative">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          className="w-full h-auto rounded-t-lg"
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

