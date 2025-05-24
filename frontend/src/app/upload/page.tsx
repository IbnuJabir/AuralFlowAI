"use client"

import { useState } from "react"
import { useMutation } from "@tanstack/react-query"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { CheckCircle, AlertCircle, Loader2 } from "lucide-react"
import { UploadTab } from "@/components/upload-tab"
import { LinkTab } from "@/components/link-tab"
import { submitVoiceClone } from "@/services/api"
import type { UploadRequest } from "@/types/upload"

export default function UploadPage() {
  const [activeTab, setActiveTab] = useState<"upload" | "link">("upload")
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [selectedLink, setSelectedLink] = useState<string>("")

  const mutation = useMutation({
    mutationFn: submitVoiceClone,
    onSuccess: (data) => {
      console.log("Success:", data)
      // Reset form
      setSelectedFile(null)
      setSelectedLink("")
    },
    onError: (error) => {
      console.error("Error:", error)
    },
  })

  const handleTabChange = (value: string) => {
    // Clear data when switching tabs
    setSelectedFile(null)
    setSelectedLink("")
    setActiveTab(value as "upload" | "link")
    mutation.reset()
  }

  const handleFileSelect = (file: File, source: "local" | "google-drive") => {
    setSelectedFile(file)

    const request: UploadRequest = {
      type: "file",
      data: file,
      source,
    }

    mutation.mutate(request)
  }

  const handleLinkSubmit = (link: string, platform: string) => {
    setSelectedLink(link)

    const request: UploadRequest = {
      type: "link",
      data: link,
      source: platform as any,
    }

    mutation.mutate(request)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-muted/20 p-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent mb-2">
            VIDUS AI
          </h1>
          <p className="text-xl text-muted-foreground">Upload your video or audio for voice cloning and dubbing</p>
        </div>

        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <span>Upload Content</span>
              {mutation.isPending && <Loader2 className="h-5 w-5 animate-spin" />}
            </CardTitle>
            <CardDescription>
              Choose to upload a file from your device or paste a link from supported platforms
            </CardDescription>
          </CardHeader>

          <CardContent>
            <Tabs value={activeTab} onValueChange={handleTabChange} className="w-full">
              <TabsList className="grid w-full grid-cols-2 mb-6">
                <TabsTrigger value="upload" className="flex items-center gap-2">
                  📁 Upload File
                </TabsTrigger>
                <TabsTrigger value="link" className="flex items-center gap-2">
                  🔗 Paste Link
                </TabsTrigger>
              </TabsList>

              <TabsContent value="upload" className="space-y-4">
                <UploadTab onFileSelect={handleFileSelect} isLoading={mutation.isPending} />

                {selectedFile && (
                  <Alert>
                    <CheckCircle className="h-4 w-4" />
                    <AlertDescription>
                      Selected: {selectedFile.name} ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
                    </AlertDescription>
                  </Alert>
                )}
              </TabsContent>

              <TabsContent value="link" className="space-y-4">
                <LinkTab onLinkSubmit={handleLinkSubmit} isLoading={mutation.isPending} />

                {selectedLink && (
                  <Alert>
                    <CheckCircle className="h-4 w-4" />
                    <AlertDescription>Processing link: {selectedLink}</AlertDescription>
                  </Alert>
                )}
              </TabsContent>
            </Tabs>

            {mutation.isError && (
              <Alert variant="destructive" className="mt-4">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  {mutation.error instanceof Error
                    ? mutation.error.message
                    : "An error occurred while processing your request"}
                </AlertDescription>
              </Alert>
            )}

            {mutation.isSuccess && (
              <Alert className="mt-4">
                <CheckCircle className="h-4 w-4" />
                <AlertDescription>{mutation.data.message || "Successfully submitted for processing!"}</AlertDescription>
              </Alert>
            )}
          </CardContent>
        </Card>

        <div className="mt-8 text-center text-sm text-muted-foreground">
          <p>Supported formats: MP4, AVI, MOV, WMV, MP3, WAV • Maximum file size: 100MB</p>
        </div>
      </div>
    </div>
  )
}
