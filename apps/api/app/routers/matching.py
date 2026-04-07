"""Matching and analysis endpoints."""

import time

from fastapi import APIRouter, HTTPException

from app.schemas.cv import CVData, JobDescription
from app.schemas.responses import APIResponse, MatchResultResponse, MatchResult
from app.services.embedder import OllamaEmbedder
from app.services.matcher import MatchService
from app.services.llm_service import LLMService

router = APIRouter(prefix="/matching")


@router.post("/analyze", response_model=APIResponse[MatchResultResponse])
async def analyze_match(
    cv_data: CVData,
    job_data: JobDescription,
) -> APIResponse[MatchResultResponse]:
    """
    Analyze compatibility between a CV and a job description.

    Calculates a match score based on:
    - Skills compatibility (40%)
    - Experience alignment (30%)
    - Education fit (15%)
    - Overall profile match (15%)

    Uses semantic embeddings for accurate comparison.
    """
    start_time = time.time()

    try:
        # Initialize services
        embedder = OllamaEmbedder()
        matcher = MatchService()

        # Check Ollama availability
        if not await embedder.health_check():
            raise HTTPException(
                status_code=503,
                detail="Ollama service not available. Please ensure Ollama is running.",
            )

        # Convert to dicts for processing
        cv_dict = cv_data.model_dump()
        job_dict = job_data.model_dump()

        # Generate embeddings and calculate similarities
        embeddings_result = await embedder.embed_sections(cv_dict, job_dict)

        # Calculate comprehensive match
        match_result = matcher.calculate_match(
            cv_data, job_dict, embeddings_result
        )

        # Optionally enhance with LLM insights (can be slow)
        try:
            llm_service = LLMService()
            llm_insights = await llm_service.analyze_gaps(
                cv_dict, job_dict, match_result.overall_score
            )
            # Add LLM insights to analysis
            if match_result.analysis:
                match_result.analysis.recommendations.append(
                    f"💡 Insight IA: {llm_insights.get('llm_analysis', '')[:200]}"
                )
        except Exception:
            # LLM enhancement is optional
            pass

        processing_time = int((time.time() - start_time) * 1000)

        return APIResponse(
            success=True,
            data=MatchResultResponse(
                match_result=match_result,
                processing_time_ms=processing_time,
            ),
            message=f"Match analysis completed. Overall score: {match_result.overall_score:.1f}%",
            processing_time_ms=processing_time,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze match: {str(e)}",
        )


@router.post("/quick-score")
async def quick_score(
    cv_text: str,
    job_text: str,
) -> dict:
    """
    Quick compatibility score without full structured parsing.

    Useful for rapid comparisons when full CV data is not available.
    """
    start_time = time.time()

    try:
        embedder = OllamaEmbedder()

        if not await embedder.health_check():
            return {
                "error": "Ollama not available",
                "score": None,
            }

        # Simple embedding comparison
        cv_embedding = await embedder.embed(cv_text[:2000])
        job_embedding = await embedder.embed(job_text[:2000])

        from app.services.matcher import compute_similarity

        similarity = compute_similarity(cv_embedding, job_embedding)
        score = (similarity + 1) / 2 * 100

        return {
            "score": round(score, 1),
            "processing_time_ms": int((time.time() - start_time) * 1000),
        }

    except Exception as e:
        return {
            "error": str(e),
            "score": None,
        }
