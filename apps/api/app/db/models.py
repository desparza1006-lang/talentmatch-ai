"""SQLAlchemy database models."""

import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


def generate_uuid() -> str:
    """Generate a UUID string."""
    return str(uuid.uuid4())


class Analysis(Base):
    """Stored analysis result."""

    __tablename__ = "analyses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # CV Data
    cv_filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cv_raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    cv_structured: Mapped[dict] = mapped_column(JSON, default=dict)

    # Job Data
    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    job_company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    job_description: Mapped[str] = mapped_column(Text, nullable=False)
    job_structured: Mapped[dict] = mapped_column(JSON, default=dict)

    # Results
    match_score: Mapped[float] = mapped_column(Float, nullable=False)
    match_details: Mapped[dict] = mapped_column(JSON, default=dict)
    strengths: Mapped[list] = mapped_column(JSON, default=list)
    gaps: Mapped[list] = mapped_column(JSON, default=list)
    recommendations: Mapped[list] = mapped_column(JSON, default=list)

    # Metadata
    analysis_version: Mapped[str] = mapped_column(String(10), default="1.0")
    processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "cv_filename": self.cv_filename,
            "job_title": self.job_title,
            "job_company": self.job_company,
            "match_score": self.match_score,
            "strengths": self.strengths,
            "gaps": self.gaps,
            "recommendations": self.recommendations,
        }
