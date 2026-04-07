"""Matching service for CV-Job compatibility calculation."""

import math
from typing import Dict, List, Tuple

from app.schemas.cv import CVData
from app.schemas.responses import (
    MatchAnalysis,
    MatchResult,
    SectionScore,
    SkillComparison,
)


def compute_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Compute cosine similarity between two embeddings.

    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector

    Returns:
        Cosine similarity between -1 and 1
    """
    if not embedding1 or not embedding2:
        return 0.0

    if len(embedding1) != len(embedding2):
        # Fallback: truncate to the shortest length to avoid crashing
        min_len = min(len(embedding1), len(embedding2))
        embedding1 = embedding1[:min_len]
        embedding2 = embedding2[:min_len]

    # Compute dot product
    dot_product = sum(a * b for a, b in zip(embedding1, embedding2))

    # Compute magnitudes
    magnitude1 = math.sqrt(sum(a * a for a in embedding1))
    magnitude2 = math.sqrt(sum(b * b for b in embedding2))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


class MatchService:
    """Service for calculating CV-Job compatibility."""

    # Weights for different sections in final score
    SECTION_WEIGHTS = {
        "skills": 0.40,
        "experience": 0.30,
        "education": 0.15,
        "overall": 0.15,
    }

    def __init__(self):
        pass

    def calculate_match(
        self,
        cv_data: CVData,
        job_data: dict,
        embeddings_result: dict,
    ) -> MatchResult:
        """
        Calculate comprehensive match between CV and Job.

        Args:
            cv_data: Structured CV data
            job_data: Structured job data
            embeddings_result: Result from embedder with similarities

        Returns:
            MatchResult with scores and analysis
        """
        similarities = embeddings_result.get("similarities", {})

        # Calculate section scores (convert similarity -1,1 to 0,100)
        section_scores = []

        skills_sim = similarities.get("skills", 0)
        skills_score = SectionScore(
            name="Habilidades",
            score=self._normalize_score(skills_sim),
            weight=self.SECTION_WEIGHTS["skills"],
            details=f"{int(self._normalize_score(skills_sim))}% de match en habilidades técnicas",
        )
        section_scores.append(skills_score)

        exp_sim = similarities.get("experience", 0)
        exp_score = SectionScore(
            name="Experiencia",
            score=self._normalize_score(exp_sim),
            weight=self.SECTION_WEIGHTS["experience"],
            details=f"{int(self._normalize_score(exp_sim))}% de match en experiencia",
        )
        section_scores.append(exp_score)

        edu_sim = similarities.get("education", 0)
        edu_score = SectionScore(
            name="Educación",
            score=self._normalize_score(edu_sim),
            weight=self.SECTION_WEIGHTS["education"],
            details=f"{int(self._normalize_score(edu_sim))}% de match en educación",
        )
        section_scores.append(edu_score)

        overall_sim = similarities.get("overall", 0)
        overall_score = SectionScore(
            name="Perfil General",
            score=self._normalize_score(overall_sim),
            weight=self.SECTION_WEIGHTS["overall"],
            details="Compatibilidad general del perfil",
        )
        section_scores.append(overall_score)

        # Calculate weighted final score
        final_score = sum(
            s.score * s.weight for s in section_scores
        )

        # Analyze skills
        skill_comparison = self._compare_skills(cv_data.skills, job_data)

        # Generate analysis
        analysis = self._generate_analysis(
            cv_data, job_data, skill_comparison, section_scores
        )

        # Generate summary
        summary = self._generate_summary(final_score, analysis)

        return MatchResult(
            overall_score=round(final_score, 1),
            section_scores=section_scores,
            analysis=analysis,
            summary=summary,
        )

    def _normalize_score(self, similarity: float) -> float:
        """Convert cosine similarity (-1 to 1) to percentage (0 to 100)."""
        # Cosine similarity ranges from -1 to 1
        # Normalize to 0-100
        normalized = (similarity + 1) / 2 * 100
        return max(0, min(100, normalized))

    def _compare_skills(
        self, cv_skills: object, job_data: dict
    ) -> SkillComparison:
        """Compare CV skills with job requirements."""
        # Extract all CV skills (lowercase for comparison)
        cv_tech = set(s.lower() for s in cv_skills.technical)
        cv_tools = set(s.lower() for s in cv_skills.tools)
        cv_all = cv_tech.union(cv_tools)

        # Job requirements
        required = set(s.lower() for s in job_data.get("required_skills", []))
        preferred = set(s.lower() for s in job_data.get("preferred_skills", []))
        job_all = required.union(preferred)

        # Find matches
        matched = []
        missing = []
        extra = []

        # Check required skills
        for skill in required:
            if any(skill in cv_skill or cv_skill in skill for cv_skill in cv_all):
                matched.append(skill)
            else:
                missing.append(skill)

        # Check preferred skills (bonus)
        for skill in preferred:
            if any(skill in cv_skill or cv_skill in skill for cv_skill in cv_all):
                if skill not in matched:
                    matched.append(skill)

        # Find extra skills
        for cv_skill in cv_all:
            if not any(
                cv_skill in job_skill or job_skill in cv_skill for job_skill in job_all
            ):
                extra.append(cv_skill)

        # Calculate match percentage
        if required:
            match_pct = len([m for m in matched if m in required]) / len(required) * 100
        else:
            match_pct = 100 if matched else 0

        return SkillComparison(
            matched=list(set(matched)),
            missing=list(set(missing)),
            extra=list(set(extra))[:10],  # Limit extra skills
            match_percentage=round(match_pct, 1),
        )

    def _generate_analysis(
        self,
        cv_data: CVData,
        job_data: dict,
        skill_comparison: SkillComparison,
        section_scores: List[SectionScore],
    ) -> MatchAnalysis:
        """Generate detailed analysis of the match."""
        strengths = []
        gaps = []
        recommendations = []

        # Analyze skills
        if skill_comparison.match_percentage >= 80:
            strengths.append(
                f"Excelente match de habilidades ({skill_comparison.match_percentage:.0f}%): "
                f"dominas la mayoría de las tecnologías requeridas."
            )
        elif skill_comparison.match_percentage >= 50:
            strengths.append(
                f"Buena base técnica con {len(skill_comparison.matched)} habilidades coincidentes."
            )
            gaps.append(
                f"Faltan {len(skill_comparison.missing)} habilidades requeridas: "
                f"{', '.join(skill_comparison.missing[:5])}"
            )
        else:
            gaps.append(
                f"Diferencia significativa en habilidades técnicas. "
                f"Solo {skill_comparison.match_percentage:.0f}% de match."
            )

        # Analyze extra skills
        if skill_comparison.extra:
            strengths.append(
                f"Tienes {len(skill_comparison.extra)} habilidades adicionales que pueden diferenciarte."
            )

        # Analyze experience
        exp_score = next((s for s in section_scores if s.name == "Experiencia"), None)
        if exp_score:
            if exp_score.score >= 80:
                strengths.append(
                    "Tu experiencia previa se alinea muy bien con los requisitos del puesto."
                )
            elif exp_score.score >= 60:
                strengths.append("Tienes experiencia relevante para el puesto.")
            else:
                gaps.append(
                    "Tu experiencia actual no se alinea completamente con lo que buscan."
                )
                recommendations.append(
                    "Destaca proyectos personales o freelance relacionados con el puesto."
                )

        # Check experience years requirement
        min_years = job_data.get("min_experience_years")
        if min_years:
            # Calculate total experience
            total_exp = self._calculate_total_experience(cv_data.experience)
            if total_exp >= min_years:
                strengths.append(
                    f"Cumples con los {min_years}+ años de experiencia requeridos."
                )
            else:
                gaps.append(
                    f"El puesto requiere {min_years}+ años, tienes ~{total_exp} años."
                )
                recommendations.append(
                    "Enfatiza la calidad y profundidad de tu experiencia actual."
                )

        # Education analysis
        edu_score = next((s for s in section_scores if s.name == "Educación"), None)
        if edu_score and edu_score.score < 60:
            recommendations.append(
                "Considera obtener certificaciones relevantes para el sector."
            )

        # General recommendations
        if skill_comparison.missing:
            top_missing = skill_comparison.missing[:3]
            recommendations.append(
                f"Prioriza aprender: {', '.join(top_missing)}. "
                f"Hay cursos en línea de 4-8 semanas."
            )

        if not strengths:
            strengths.append(
                "Tu perfil tiene potencial. Considera adaptar tu CV para destacar mejor tus logros."
            )

        return MatchAnalysis(
            strengths=strengths[:5],
            gaps=gaps[:5],
            recommendations=recommendations[:5],
            skill_comparison=skill_comparison,
        )

    def _calculate_total_experience(self, experiences: list) -> int:
        """Calculate total years of experience."""
        total_months = 0
        for exp in experiences:
            total_months += exp.duration_months or 0
        return total_months // 12

    def _generate_summary(self, score: float, analysis: MatchAnalysis) -> str:
        """Generate executive summary of the match."""
        if score >= 80:
            level = "excelente"
            emoji = "🌟"
        elif score >= 60:
            level = "bueno"
            emoji = "✅"
        elif score >= 40:
            level = "moderado"
            emoji = "⚠️"
        else:
            level = "bajo"
            emoji = "❌"

        summary = (
            f"{emoji} Compatibilidad {level} ({score:.0f}%). "
            f"{len(analysis.strengths)} fortalezas identificadas, "
            f"{len(analysis.gaps)} áreas de mejora. "
        )

        if analysis.skill_comparison.match_percentage >= 70:
            summary += "Tienes un sólido match técnico. "
        elif analysis.skill_comparison.match_percentage >= 40:
            summary += "Necesitas desarrollar algunas habilidades clave. "
        else:
            summary += "Hay una brecha técnica importante a cerrar. "

        if analysis.recommendations:
            summary += f"Recomendación principal: {analysis.recommendations[0]}"

        return summary
