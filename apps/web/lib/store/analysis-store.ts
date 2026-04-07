import { create } from "zustand";
import { persist } from "zustand/middleware";
import { CVData, JobDescription, MatchResult } from "@/types";

interface AnalysisState {
  // Current analysis
  cvData: CVData | null;
  jobData: JobDescription | null;
  matchResult: MatchResult | null;
  isAnalyzing: boolean;
  error: string | null;

  // Actions
  setCVData: (data: CVData | null) => void;
  setJobData: (data: JobDescription | null) => void;
  setMatchResult: (result: MatchResult | null) => void;
  setIsAnalyzing: (analyzing: boolean) => void;
  setError: (error: string | null) => void;
  
  // History
  addToHistory: (analysis: AnalysisHistoryItem) => void;
  clearCurrent: () => void;
  reset: () => void;
}

interface AnalysisHistoryItem {
  id: string;
  timestamp: number;
  cvName?: string;
  jobTitle: string;
  score: number;
}

export const useAnalysisStore = create<AnalysisState>()(
  persist(
    (set, get) => ({
      // Initial state
      cvData: null,
      jobData: null,
      matchResult: null,
      isAnalyzing: false,
      error: null,

      // Actions
      setCVData: (data) => set({ cvData: data }),
      setJobData: (data) => set({ jobData: data }),
      setMatchResult: (result) => set({ matchResult: result }),
      setIsAnalyzing: (analyzing) => set({ isAnalyzing: analyzing }),
      setError: (error) => set({ error }),

      addToHistory: (analysis) => {
        // This would add to a history array in a real implementation
        console.log("Added to history:", analysis);
      },

      clearCurrent: () =>
        set({
          cvData: null,
          jobData: null,
          matchResult: null,
          error: null,
        }),

      reset: () =>
        set({
          cvData: null,
          jobData: null,
          matchResult: null,
          isAnalyzing: false,
          error: null,
        }),
    }),
    {
      name: "talentmatch-analysis",
      partialize: (state) => ({
        cvData: state.cvData,
        jobData: state.jobData,
        matchResult: state.matchResult,
      }),
    }
  )
);
