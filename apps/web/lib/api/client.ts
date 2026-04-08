import { APIResponse, CVData, JobDescription, MatchResultResponse } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

if (!API_BASE_URL) {
  throw new Error(
    "NEXT_PUBLIC_API_URL environment variable is not defined. " +
    "Please set it in your Vercel project settings."
  );
}

class APIClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async fetch<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<APIResponse<T>> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const response = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Unknown error" }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  async uploadCV(file: File): Promise<APIResponse<CVData>> {
    const formData = new FormData();
    formData.append("file", file);

    return this.fetch<CVData>("/cv/upload", {
      method: "POST",
      body: formData,
    });
  }

  async parseCVText(text: string): Promise<APIResponse<CVData>> {
    const formData = new FormData();
    formData.append("text", text);

    return this.fetch<CVData>("/cv/parse-text", {
      method: "POST",
      body: formData,
    });
  }

  async analyzeMatch(
    cvData: CVData,
    jobData: JobDescription
  ): Promise<APIResponse<MatchResultResponse>> {
    return this.fetch<MatchResultResponse>("/matching/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ cv_data: cvData, job_data: jobData }),
    });
  }

  async healthCheck(): Promise<{ status: string; version: string }> {
    const response = await fetch(`${this.baseUrl}/health`);
    return response.json();
  }
}

export const api = new APIClient(API_BASE_URL);
