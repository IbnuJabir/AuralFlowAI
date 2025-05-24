"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Link, CheckCircle, AlertCircle } from "lucide-react"
import { validateVideoLink, getPlatformIcon } from "@/utils/link-validation"
import type { LinkValidation } from "@/types/upload"

interface LinkTabProps {
  onLinkSubmit: (link: string, platform: string) => void
  isLoading: boolean
}

export function LinkTab({ onLinkSubmit, isLoading }: LinkTabProps) {
  const [link, setLink] = useState("")
  const [validation, setValidation] = useState<LinkValidation>({ isValid: false })

  const handleLinkChange = (value: string) => {
    setLink(value)
    if (value.trim()) {
      setValidation(validateVideoLink(value))
    } else {
      setValidation({ isValid: false })
    }
  }

  const handleSubmit = () => {
    if (validation.isValid && validation.platform) {
      onLinkSubmit(link, validation.platform)
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardContent className="pt-6">
          <div className="space-y-4">
            <div className="flex items-center gap-2 mb-4">
              <Link className="h-5 w-5 text-primary" />
              <h3 className="text-lg font-semibold">Paste Video Link</h3>
            </div>

            <div className="space-y-2">
              <Input
                placeholder="Paste YouTube, Vimeo, or Google Drive link here..."
                value={link}
                onChange={(e) => handleLinkChange(e.target.value)}
                disabled={isLoading}
                className="text-base"
              />

              {link && validation.isValid && validation.platform && (
                <div className="flex items-center gap-2 text-sm text-green-600">
                  <CheckCircle className="h-4 w-4" />
                  <span>
                    {getPlatformIcon(validation.platform)} Valid {validation.platform} link detected
                  </span>
                </div>
              )}

              {link && !validation.isValid && validation.error && (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{validation.error}</AlertDescription>
                </Alert>
              )}
            </div>

            <Button onClick={handleSubmit} disabled={!validation.isValid || isLoading} className="w-full">
              {isLoading ? "Processing..." : "Submit Link"}
            </Button>
          </div>
        </CardContent>
      </Card>

      <div className="text-sm text-muted-foreground">
        <h4 className="font-medium mb-2">Supported platforms:</h4>
        <ul className="space-y-1">
          <li className="flex items-center gap-2">
            🎥 <span>YouTube (youtube.com, youtu.be)</span>
          </li>
          <li className="flex items-center gap-2">
            📹 <span>Vimeo (vimeo.com)</span>
          </li>
          <li className="flex items-center gap-2">
            💾 <span>Google Drive (drive.google.com)</span>
          </li>
        </ul>
      </div>
    </div>
  )
}
