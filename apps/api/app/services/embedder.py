"""Ollama embedding service for semantic matching."""

import asyncio
from typing import List, Optional

import httpx

from app.config import settings


class OllamaEmbedder:
    """Client for Ollama embedding models."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: int = 120,
    ):
        self.base_url = base_url or settings.ollama_base_url
        self.model = model or settings.ollama_embedding_model
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def health_check(self) -> bool:
        """Check if Ollama is available."""
        try:
            client = await self._get_client()
            response = await client.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except Exception:
            return False

    async def embed(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector

        Raises:
            RuntimeError: If embedding generation fails
        """
        # Ollama can return inconsistent dimensions for empty strings.
        safe_text = text[:8192] if text.strip() else " "

        try:
            client = await self._get_client()

            response = await client.post(
                f"{self.base_url}/api/embeddings",
                json={
                    "model": self.model,
                    "prompt": safe_text,
                },
            )

            response.raise_for_status()
            data = response.json()

            embedding = data.get("embedding")
            if not isinstance(embedding, list) or len(embedding) == 0:
                raise RuntimeError("Empty or invalid embedding returned by Ollama")

            return embedding

        except httpx.HTTPError as e:
            raise RuntimeError(f"Failed to generate embedding: {e}")
        except KeyError:
            raise RuntimeError("Invalid response from Ollama API")

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        # Process sequentially to avoid overwhelming Ollama
        embeddings = []
        for text in texts:
            embedding = await self.embed(text)
            embeddings.append(embedding)
            # Small delay to be nice to the API
            await asyncio.sleep(0.1)
        return embeddings

    async def embed_sections(
        self, cv_data: dict, job_data: dict
    ) -> dict:
        """
        Embed specific sections of CV and Job for comparison.

        Args:
            cv_data: Structured CV data
            job_data: Structured job data

        Returns:
            Dictionary with embeddings for each section
        """
        from app.services.matcher import compute_similarity

        # Prepare texts for each section
        texts = {
            "cv_full": self._prepare_cv_text(cv_data),
            "cv_skills": self._prepare_skills_text(cv_data.get("skills", {})),
            "cv_experience": self._prepare_experience_text(
                cv_data.get("experience", [])
            ),
            "cv_education": self._prepare_education_text(
                cv_data.get("education", [])
            ),
            "job_full": self._prepare_job_text(job_data),
            "job_skills": self._prepare_job_skills_text(job_data),
            "job_experience": self._prepare_job_experience_text(job_data),
            "job_education": self._prepare_job_education_text(job_data),
        }

        # Generate embeddings
        embeddings = {}
        for key, text in texts.items():
            embeddings[key] = await self.embed(text)

        # Compute similarities
        results = {
            "embeddings": embeddings,
            "similarities": {
                "overall": compute_similarity(
                    embeddings["cv_full"], embeddings["job_full"]
                ),
                "skills": compute_similarity(
                    embeddings["cv_skills"], embeddings["job_skills"]
                ),
                "experience": compute_similarity(
                    embeddings["cv_experience"], embeddings["job_experience"]
                ),
                "education": compute_similarity(
                    embeddings["cv_education"], embeddings["job_education"]
                ),
            },
        }

        return results

    def _prepare_cv_text(self, cv_data: dict) -> str:
        """Prepare full CV text for embedding."""
        parts = []

        # Summary
        summary = cv_data.get("summary", "")
        if summary:
            parts.append(f"Perfil: {summary}")

        # Skills
        skills = cv_data.get("skills", {})
        if skills:
            tech_skills = skills.get("technical", [])
            soft_skills = skills.get("soft", [])
            if tech_skills:
                parts.append(f"Habilidades técnicas: {', '.join(tech_skills)}")
            if soft_skills:
                parts.append(f"Habilidades blandas: {', '.join(soft_skills)}")

        # Experience
        experiences = cv_data.get("experience", [])
        if experiences:
            exp_texts = []
            for exp in experiences[:3]:  # Top 3 experiences
                title = exp.get("title", "")
                company = exp.get("company", "")
                desc = exp.get("description", "")
                exp_texts.append(f"{title} en {company}: {desc}")
            parts.append(f"Experiencia: {' '.join(exp_texts)}")

        return "\n".join(parts)

    def _prepare_skills_text(self, skills: dict) -> str:
        """Prepare skills text for embedding."""
        all_skills = []
        all_skills.extend(skills.get("technical", []))
        all_skills.extend(skills.get("tools", []))
        all_skills.extend(skills.get("soft", []))
        return " ".join(all_skills)

    def _prepare_experience_text(self, experiences: list) -> str:
        """Prepare experience text for embedding."""
        texts = []
        for exp in experiences:
            texts.append(exp.get("title", ""))
            texts.append(exp.get("description", ""))
        return " ".join(texts)

    def _prepare_education_text(self, education: list) -> str:
        """Prepare education text for embedding."""
        texts = []
        for edu in education:
            texts.append(edu.get("degree", ""))
            texts.append(edu.get("field", ""))
        return " ".join(texts)

    def _prepare_job_text(self, job_data: dict) -> str:
        """Prepare full job text for embedding."""
        parts = [
            f"Título: {job_data.get('title', '')}",
            f"Descripción: {job_data.get('description', '')}",
        ]

        required = job_data.get("required_skills", [])
        if required:
            parts.append(f"Habilidades requeridas: {', '.join(required)}")

        return "\n".join(parts)

    def _prepare_job_skills_text(self, job_data: dict) -> str:
        """Prepare job skills text for embedding."""
        skills = job_data.get("required_skills", []) + job_data.get(
            "preferred_skills", []
        )
        return " ".join(skills)

    def _prepare_job_experience_text(self, job_data: dict) -> str:
        """Prepare job experience text for embedding."""
        description = job_data.get("description", "").lower()
        # Extract experience requirements from description
        return description

    def _prepare_job_education_text(self, job_data: dict) -> str:
        """Prepare job education text for embedding."""
        description = job_data.get("description", "").lower()
        return description

    async def close(self):
        """Close HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
