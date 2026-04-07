"""Response schemas for API endpoints."""

from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Generic API response wrapper."""

    success: bool = Field(..., description="Whether the request was successful")
    data: Optional[T] = Field(None, description="Response data")
    message: Optional[str] = Field(None, description="Status message")
    errors: Optional[List[str]] = Field(None, description="Error messages if any")
    processing_time_ms: Optional[int] = Field(
        None, description="Processing time in milliseconds"
    )


class SkillComparison(BaseModel):
    """Skill comparison between CV and job."""

    matched: List[str] = Field(default_factory=list, description="Skills that match")
    missing: List[str] = Field(
        default_factory=list, description="Required skills not found in CV"
    )
    extra: List[str] = Field(
        default_factory=list, description="Skills in CV not required for job"
    )
    match_percentage: float = Field(
        0.0, description="Percentage of required skills matched"
    )


class SectionScore(BaseModel):
    """Score for a specific section."""

    name: str = Field(..., description="Section name")
    score: float = Field(..., description="Score from 0-100")
    weight: float = Field(..., description="Weight in overall calculation")
    details: Optional[str] = Field(None, description="Additional details")


class MatchAnalysis(BaseModel):
    """Detailed analysis of the match."""

    strengths: List[str] = Field(default_factory=list, description="Candidate strengths")
    gaps: List[str] = Field(default_factory=list, description="Identified gaps")
    recommendations: List[str] = Field(
        default_factory=list, description="Actionable recommendations"
    )
    skill_comparison: SkillComparison = Field(
        default_factory=SkillComparison, description="Skill comparison details"
    )


class MatchResult(BaseModel):
    """Complete match result."""

    overall_score: float = Field(
        ..., description="Overall compatibility score (0-100)", ge=0, le=100
    )
    section_scores: List[SectionScore] = Field(
        default_factory=list, description="Scores by section"
    )
    analysis: MatchAnalysis = Field(
        default_factory=MatchAnalysis, description="Detailed analysis"
    )
    summary: str = Field("", description="Executive summary of the match")


class CVParseResponse(BaseModel):
    """Response for CV parsing endpoint."""

    cv_data: "CVData"  # type: ignore # Forward reference handled in __init__
    processing_time_ms: int


class MatchResultResponse(BaseModel):
    """Response for matching endpoint."""

    match_result: MatchResult
    processing_time_ms: int


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    debug: bool
    ollama_available: Optional[bool] = None


# Re-export CVData for type resolution
from app.schemas.cv import CVData  # noqa: E402

CVParseResponse.model_rebuild()
