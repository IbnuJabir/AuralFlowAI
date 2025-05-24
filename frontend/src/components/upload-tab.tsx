"use client"

import type React from "react"

import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Upload, FileVideo, HardDrive } from "lucide-react"
import { cn } from "@/lib/utils"

interface UploadTabProps {
  onFileSelect: (file: File, source: "local" | "google-drive") => void
  isLoading: boolean
}

export function UploadTab({ onFileSelect, isLoading }: UploadTabProps) {
  const [dragActive, setDragActive] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    const files = e.dataTransfer.files
    if (files && files[0]) {
      handleFileSelection(files[0], "local")
    }
  }

  const handleFileSelection = (file: File, source: "local" | "google-drive") => {
    const validTypes = ["video/mp4", "video/avi", "video/mov", "video/wmv", "audio/mp3", "audio/wav", "audio/mpeg"]
    console.log("Selected file:", file.name)
    console.log("File size:", file.size)
    console.log("File type:", file.type)
    console.log("Source:", source)
    console.log("Valid types:", validTypes)
    if (!validTypes.includes(file.type)) {
      alert("Please select a valid video or audio file")
      return
    }

    if (file.size > 100 * 1024 * 1024) {
      // 100MB limit
      alert("File size must be less than 100MB")
      return
    }

    onFileSelect(file, source)
  }

  const handleLocalUpload = () => {
    fileInputRef.current?.click()
  }

  const handleGoogleDriveUpload = () => {
    // In a real implementation, you would integrate with Google Drive API
    alert("Google Drive integration would be implemented here")
  }

  return (
    <div className="space-y-6">
      <Card
        className={cn(
          "border-2 border-dashed transition-colors",
          dragActive ? "border-primary bg-primary/5" : "border-muted-foreground/25",
          isLoading && "opacity-50 pointer-events-none",
        )}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <CardContent className="flex flex-col items-center justify-center py-12 text-center">
          <Upload className="h-12 w-12 text-muted-foreground mb-4" />
          <h3 className="text-lg font-semibold mb-2">Drop your video or audio file here</h3>
          <p className="text-sm text-muted-foreground mb-6">Supports MP4, AVI, MOV, WMV, MP3, WAV (max 100MB)</p>

          <div className="flex gap-4">
            <Button onClick={handleLocalUpload} disabled={isLoading} className="flex items-center gap-2">
              <FileVideo className="h-4 w-4" />
              Choose from Computer
            </Button>

            <Button
              onClick={handleGoogleDriveUpload}
              variant="outline"
              disabled={isLoading}
              className="flex items-center gap-2"
            >
              <HardDrive className="h-4 w-4" />
              Choose from Google Drive
            </Button>
          </div>
        </CardContent>
      </Card>

      <input
        ref={fileInputRef}
        type="file"
        accept="video/*,audio/*"
        onChange={(e) => {
          const file = e.target.files?.[0]
          if (file) {
            handleFileSelection(file, "local")
          }
        }}
        className="hidden"
      />
    </div>
  )
}
