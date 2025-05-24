// frontend/src/services/api.ts
import axios from "axios"
import type { 
  UploadRequest, 
  ApiResponse, 
  VoiceCloneStatusResponse, 
  SupportedFormatsResponse 
} from "@/types/upload"

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api",
  timeout: 60000, // Increased timeout for file uploads
})

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to: ${config.url}`)
    return config
  },
  (error) => {
    console.error("Request error:", error)
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export async function submitVoiceClone(request: UploadRequest): Promise<ApiResponse> {
  const formData = new FormData()

  if (request.type === "file") {
    formData.append("file", request.data as File)
    formData.append("source", request.source || "local")
  } else {
    formData.append("link", request.data as string)
    formData.append("source", request.source || "unknown")
  }

  formData.append("type", request.type)
  
  if (request.target_language) {
    formData.append("target_language", request.target_language)
  }
  
  if (request.voice_settings) {
    formData.append("voice_settings", JSON.stringify(request.voice_settings))
  }

  const response = await api.post<ApiResponse>("/voice/voice-clone", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  })

  return response.data
}

export async function getVoiceCloneStatus(taskId: string): Promise<VoiceCloneStatusResponse> {
  const response = await api.get<VoiceCloneStatusResponse>(`/voice/status/${taskId}`)
  return response.data
}

export async function cancelVoiceCloneTask(taskId: string): Promise<{ success: boolean; message: string }> {
  const response = await api.delete(`/voice/task/${taskId}`)
  return response.data
}

export async function getSupportedFormats(): Promise<SupportedFormatsResponse> {
  const response = await api.get<SupportedFormatsResponse>("/voice/supported-formats")
  return response.data
}

// Polling function for task status
export async function pollTaskStatus(
  taskId: string,
  onUpdate: (status: VoiceCloneStatusResponse) => void,
  pollInterval: number = 2000 // 2 seconds
): Promise<VoiceCloneStatusResponse> {
  return new Promise((resolve, reject) => {
    const poll = async () => {
      try {
        const status = await getVoiceCloneStatus(taskId)
        onUpdate(status)

        if (status.status === "success") {
          resolve(status)
        } else if (status.status === "failure") {
          reject(new Error(status.error_message || "Task failed"))
        } else {
          // Continue polling for pending/processing states
          setTimeout(poll, pollInterval)
        }
      } catch (error) {
        reject(error)
      }
    }

    poll()
  })
}