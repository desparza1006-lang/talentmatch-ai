"""LLM service for generating insights and recommendations."""

import json
from typing import List, Optional

import httpx

from app.config import settings


class LLMService:
    """Service for interacting with Ollama LLM models."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: int = 120,
    ):
        self.base_url = base_url or settings.ollama_base_url
        self.model = model or settings.ollama_llm_model
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """
        Generate text using the LLM.

        Args:
            prompt: Input prompt
            temperature: Creativity level (0.0 - 1.0)
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text
        """
        try:
            client = await self._get_client()

            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                    },
                },
            )

            response.raise_for_status()
            data = response.json()

            return data.get("response", "").strip()

        except Exception as e:
            return f"Error generating response: {str(e)}"

    async def analyze_gaps(
        self,
        cv_data: dict,
        job_data: dict,
        match_score: float,
    ) -> dict:
        """
        Analyze gaps between CV and job using LLM.

        Args:
            cv_data: Structured CV data
            job_data: Structured job data
            match_score: Calculated match score

        Returns:
            Dictionary with LLM-generated insights
        """
        prompt = self._build_gap_analysis_prompt(cv_data, job_data, match_score)
        response = await self.generate(prompt, temperature=0.5, max_tokens=800)

        return {
            "llm_analysis": response,
            "prompt_used": prompt,
        }

    async def improve_summary(
        self,
        current_summary: Optional[str],
        cv_data: dict,
        job_data: dict,
    ) -> str:
        """
        Suggest improvements for professional summary.

        Args:
            current_summary: Current summary text
            cv_data: Full CV data
            job_data: Target job data

        Returns:
            Improved summary suggestion
        """
        prompt = f"""Eres un experto en reclutamiento tech. Mejora el siguiente resumen profesional para que destaque frente a esta oferta laboral.

OFERTA LABORAL:
Título: {job_data.get('title', 'No especificado')}
Descripción: {job_data.get('description', 'No especificada')[:500]}...

RESUMEN ACTUAL:
{current_summary or "No tiene resumen."}

EXPERIENCIA DEL CANDIDATO:
"""
        for exp in cv_data.get('experience', [])[:3]:
            prompt += f"- {exp.get('title', '')} en {exp.get('company', '')}\n"

        prompt += f"""

HABILIDADES:
Técnicas: {', '.join(cv_data.get('skills', {}).get('technical', [])[:10])}

INSTRUCCIONES:
1. Escribe un resumen profesional de máximo 4 líneas.
2. Destaca la experiencia más relevante para el puesto.
3. Incluye keywords del job description.
4. Usa un tono profesional pero cercano.
5. Muestra el valor que aportaría al equipo.

NUEVO RESUMEN:"""

        return await self.generate(prompt, temperature=0.7, max_tokens=300)

    async def generate_interview_tips(
        self,
        cv_data: dict,
        job_data: dict,
    ) -> List[str]:
        """Generate interview preparation tips."""
        prompt = f"""Genera 5 consejos específicos para preparar una entrevista para este puesto.

PUESTO: {job_data.get('title', '')}
DESCRIPCIÓN: {job_data.get('description', '')[:800]}

PERFIL DEL CANDIDATO:
- Experiencia: {len(cv_data.get('experience', []))} posiciones
- Skills: {', '.join(cv_data.get('skills', {}).get('technical', [])[:8])}

Formato: Lista numerada, cada punto en una línea nueva. Sé específico y práctico.

CONSEJOS:"""

        response = await self.generate(prompt, temperature=0.6, max_tokens=500)

        # Parse into list
        tips = []
        for line in response.split("\n"):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith("-")):
                # Remove numbering/bullets
                tip = line.lstrip("0123456789.- ")
                if tip:
                    tips.append(tip)

        return tips[:5]

    def _build_gap_analysis_prompt(
        self,
        cv_data: dict,
        job_data: dict,
        match_score: float,
    ) -> str:
        """Build prompt for gap analysis."""

        # Extract skills for context
        cv_skills = cv_data.get("skills", {})
        cv_tech = cv_skills.get("technical", [])
        cv_soft = cv_skills.get("soft", [])

        job_req = job_data.get("required_skills", [])
        job_pref = job_data.get("preferred_skills", [])

        prompt = f"""Eres un reclutador tech senior. Analiza la compatibilidad entre este candidato y el puesto.

PUNTUACIÓN GENERAL: {match_score:.0f}/100

PERFIL DEL CANDIDATO:
- Nombre: {cv_data.get('personal_info', {}).get('name', 'No especificado')}
- Resumen: {cv_data.get('summary', 'No disponible')[:300]}
- Habilidades técnicas: {', '.join(cv_tech[:15]) or 'No especificadas'}
- Habilidades blandas: {', '.join(cv_soft[:5]) or 'No especificadas'}
- Años de experiencia: {len(cv_data.get('experience', []))} posiciones registradas

OFERTA LABORAL:
- Título: {job_data.get('title', 'No especificado')}
- Habilidades requeridas: {', '.join(job_req) or 'No especificadas'}
- Habilidades preferidas: {', '.join(job_pref) or 'Ninguna'}

INSTRUCCIONES:
Proporciona un análisis breve (máximo 3 párrafos) que incluya:
1. Evaluación general del fit del candidato
2. Fortalezas clave para este puesto
3. Brechas importantes a considerar

Sé directo, profesional y constructivo. Usa español.

ANÁLISIS:"""

        return prompt

    async def close(self):
        """Close HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
