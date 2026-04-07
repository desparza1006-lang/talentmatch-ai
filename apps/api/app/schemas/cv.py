"""CV-related Pydantic schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class PersonalInfo(BaseModel):
    """Personal information extracted from CV."""

    name: Optional[str] = Field(None, description="Full name of the candidate")
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    location: Optional[str] = Field(None, description="City/Country")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    portfolio: Optional[str] = Field(None, description="Portfolio/Website URL")


class SkillSet(BaseModel):
    """Skills extracted from CV."""

    technical: List[str] = Field(default_factory=list, description="Technical skills")
    soft: List[str] = Field(default_factory=list, description="Soft skills")
    tools: List[str] = Field(default_factory=list, description="Tools and platforms")
    languages: List[dict] = Field(
        default_factory=list, description="Languages with proficiency level"
    )


class Experience(BaseModel):
    """Work experience entry."""

    company: Optional[str] = Field(None, description="Company name")
    title: Optional[str] = Field(None, description="Job title")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM or present)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM or present)")
    duration_months: Optional[int] = Field(None, description="Duration in months")
    description: Optional[str] = Field(None, description="Job description")
    technologies: List[str] = Field(
        default_factory=list, description="Technologies mentioned"
    )
    is_current: bool = Field(False, description="Whether this is the current job")


class Education(BaseModel):
    """Education entry."""

    institution: Optional[str] = Field(None, description="School/University name")
    degree: Optional[str] = Field(None, description="Degree obtained")
    field: Optional[str] = Field(None, description="Field of study")
    start_year: Optional[int] = Field(None, description="Start year")
    end_year: Optional[int] = Field(None, description="End year or expected")
    description: Optional[str] = Field(None, description="Additional details")


class CVData(BaseModel):
    """Complete structured CV data."""

    personal_info: PersonalInfo = Field(
        default_factory=PersonalInfo, description="Personal information"
    )
    summary: Optional[str] = Field(None, description="Professional summary/objective")
    skills: SkillSet = Field(default_factory=SkillSet, description="Skills")
    experience: List[Experience] = Field(
        default_factory=list, description="Work experience"
    )
    education: List[Education] = Field(default_factory=list, description="Education")
    certifications: List[str] = Field(
        default_factory=list, description="Certifications"
    )
    raw_text: str = Field("", description="Raw text extracted from CV")
    extracted_at: datetime = Field(
        default_factory=datetime.utcnow, description="Extraction timestamp"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "personal_info": {
                    "name": "Juan Pérez",
                    "email": "juan@example.com",
                    "phone": "+34 612 345 678",
                    "location": "Madrid, España",
                },
                "summary": "Desarrollador Full Stack con 5 años de experiencia...",
                "skills": {
                    "technical": ["Python", "JavaScript", "React"],
                    "soft": ["Liderazgo", "Comunicación"],
                    "tools": ["Docker", "AWS"],
                },
                "experience": [
                    {
                        "company": "Tech Corp",
                        "title": "Senior Developer",
                        "start_date": "2021-03",
                        "is_current": True,
                    }
                ],
                "raw_text": "Texto completo del CV...",
            }
        }


class JobDescription(BaseModel):
    """Job description input."""

    title: str = Field(..., description="Job title")
    company: Optional[str] = Field(None, description="Company name")
    description: str = Field(..., description="Full job description text")
    required_skills: List[str] = Field(
        default_factory=list, description="Explicitly required skills"
    )
    preferred_skills: List[str] = Field(
        default_factory=list, description="Preferred/nice-to-have skills"
    )
    min_experience_years: Optional[int] = Field(
        None, description="Minimum years of experience"
    )
    location: Optional[str] = Field(None, description="Job location")
    employment_type: Optional[str] = Field(
        None, description="Full-time, part-time, contract"
    )
