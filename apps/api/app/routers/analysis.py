"""Additional analysis endpoints."""

from fastapi import APIRouter, HTTPException

from app.schemas.cv import CVData, JobDescription
from app.services.llm_service import LLMService

router = APIRouter(prefix="/analysis")


@router.post("/improve-summary")
async def improve_professional_summary(
    cv_data: CVData,
    job_data: JobDescription,
) -> dict:
    """
    Generate an improved professional summary tailored for a specific job.

    Uses LLM to rewrite the summary highlighting relevant experience
    and incorporating job keywords.
    """
    try:
        llm_service = LLMService()

        improved_summary = await llm_service.improve_summary(
            cv_data.summary,
            cv_data.model_dump(),
            job_data.model_dump(),
        )

        return {
            "success": True,
            "original_summary": cv_data.summary,
            "improved_summary": improved_summary,
            "tips": [
                "Personaliza este resumen para cada aplicación",
                "Mide su efectividad por la tasa de respuesta",
                "A/B test diferentes versiones",
            ],
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate summary: {str(e)}",
        )


@router.post("/interview-tips")
async def get_interview_tips(
    cv_data: CVData,
    job_data: JobDescription,
) -> dict:
    """
    Generate personalized interview preparation tips.

    Based on the candidate's profile and the specific job requirements.
    """
    try:
        llm_service = LLMService()

        tips = await llm_service.generate_interview_tips(
            cv_data.model_dump(),
            job_data.model_dump(),
        )

        return {
            "success": True,
            "tips": tips,
            "general_advice": [
                "Investiga la empresa: cultura, productos, noticias recientes",
                "Prepara preguntas inteligentes sobre el rol y el equipo",
                "Practica el 'Cuéntame sobre ti' enfocado en logros medibles",
                "Ten ejemplos concretos usando el método STAR",
            ],
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate tips: {str(e)}",
        )


@router.get("/skills-market-trends")
async def get_skills_trends() -> dict:
    """
    Get current market trends for tech skills.

    Returns information about in-demand skills (mock data for MVP).
    """
    # In a real implementation, this would fetch from a database or external API
    return {
        "high_demand": [
            {"skill": "Python", "growth": "+15%", "category": "Backend"},
            {"skill": "React", "growth": "+12%", "category": "Frontend"},
            {"skill": "AWS", "growth": "+20%", "category": "Cloud"},
            {"skill": "Docker", "growth": "+18%", "category": "DevOps"},
            {"skill": "Machine Learning", "growth": "+25%", "category": "Data"},
        ],
        "emerging": [
            {"skill": "Rust", "growth": "+35%", "category": "Systems"},
            {"skill": "Next.js", "growth": "+30%", "category": "Frontend"},
            {"skill": "LangChain", "growth": "+40%", "category": "AI/ML"},
        ],
        "last_updated": "2024-01-15",
    }
