export interface PersonalInfo {
  name?: string;
  email?: string;
  phone?: string;
  location?: string;
  linkedin?: string;
  portfolio?: string;
}

export interface SkillSet {
  technical: string[];
  soft: string[];
  tools: string[];
  languages: Array<{ name: string; level: string }>;
}

export interface Experience {
  company?: string;
  title?: string;
  start_date?: string;
  end_date?: string;
  duration_months?: number;
  description?: string;
  technologies: string[];
  is_current: boolean;
}

export interface Education {
  institution?: string;
  degree?: string;
  field?: string;
  start_year?: number;
  end_year?: number;
  description?: string;
}

export interface CVData {
  personal_info: PersonalInfo;
  summary?: string;
  skills: SkillSet;
  experience: Experience[];
  education: Education[];
  certifications: string[];
  raw_text: string;
  extracted_at: string;
}

export interface JobDescription {
  title: string;
  company?: string;
  description: string;
  required_skills: string[];
  preferred_skills: string[];
  min_experience_years?: number;
  location?: string;
  employment_type?: string;
}

export interface SkillComparison {
  matched: string[];
  missing: string[];
  extra: string[];
  match_percentage: number;
}

export interface SectionScore {
  name: string;
  score: number;
  weight: number;
  details?: string;
}

export interface MatchAnalysis {
  strengths: string[];
  gaps: string[];
  recommendations: string[];
  skill_comparison: SkillComparison;
}

export interface MatchResult {
  overall_score: number;
  section_scores: SectionScore[];
  analysis: MatchAnalysis;
  summary: string;
}

export interface APIResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  errors?: string[];
  processing_time_ms?: number;
}

export interface MatchResultResponse {
  match_result: MatchResult;
  processing_time_ms: number;
}

export interface AnalysisHistory {
  id: string;
  created_at: string;
  cv_filename?: string;
  job_title: string;
  job_company?: string;
  match_score: number;
}
