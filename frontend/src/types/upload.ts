// frontend/src/types/upload.ts

export interface LinkValidation {
  isValid: boolean
  platform?: "youtube" | "vimeo" | "google-drive"
  error?: string
}

export interface UploadRequest {
  type: "file" | "link"
  data: File | string
  source?: "local" | "google-drive" | "youtube" | "vimeo"
  target_language?: string
  voice_settings?: Record<string, any>
}

export interface ApiResponse {
  success: boolean
  message: string
  task_id?: string
  status: string
  file_path?: string
  original_filename?: string
  processing_time?: number
  metadata?: {
    file_size?: number
    file_type?: string
    is_audio?: boolean
    is_video?: boolean
    source?: string
    target_language?: string
  }
  created_at?: string
}

export interface VoiceCloneStatusResponse {
  task_id: string
  status: string
  progress?: number // 0-100
  result_url?: string
  error_message?: string
  estimated_completion?: string
}

export interface SupportedFormatsResponse {
  audio_formats: string[]
  video_formats: string[]
  max_file_size: string
  supported_languages: string[]
}