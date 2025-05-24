import type { LinkValidation } from "@/types/upload"

export function validateVideoLink(url: string): LinkValidation {
  if (!url.trim()) {
    return { isValid: false, error: "Please enter a URL" }
  }

  try {
    const urlObj = new URL(url)

    // YouTube validation
    if (urlObj.hostname.includes("youtube.com") || urlObj.hostname.includes("youtu.be")) {
      return { isValid: true, platform: "youtube" }
    }

    // Vimeo validation
    if (urlObj.hostname.includes("vimeo.com")) {
      return { isValid: true, platform: "vimeo" }
    }

    // Google Drive validation
    if (urlObj.hostname.includes("drive.google.com")) {
      return { isValid: true, platform: "google-drive" }
    }

    return {
      isValid: false,
      error: "Only YouTube, Vimeo, and Google Drive links are supported",
    }
  } catch {
    return { isValid: false, error: "Please enter a valid URL" }
  }
}

export function getPlatformIcon(platform: string) {
  switch (platform) {
    case "youtube":
      return "🎥"
    case "vimeo":
      return "📹"
    case "google-drive":
      return "💾"
    default:
      return "🔗"
  }
}
