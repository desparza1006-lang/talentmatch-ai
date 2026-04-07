"""PDF parsing service using pdfplumber."""

import io
import re
from typing import Tuple

import pdfplumber

from app.config import settings


class CVParser:
    """Parser for CV PDF files."""

    def __init__(self):
        self.max_pages = settings.max_cv_pages

    async def parse_pdf(self, file_content: bytes) -> Tuple[str, dict]:
        """
        Parse PDF file and extract text with metadata.

        Args:
            file_content: Raw PDF bytes

        Returns:
            Tuple of (extracted_text, metadata)

        Raises:
            ValueError: If PDF cannot be parsed or exceeds page limit
        """
        try:
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                num_pages = len(pdf.pages)

                if num_pages > self.max_pages:
                    raise ValueError(
                        f"PDF has {num_pages} pages. Maximum allowed is {self.max_pages}."
                    )

                # Extract text from all pages
                pages_text = []
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        pages_text.append(text)

                full_text = "\n\n".join(pages_text)

                # Clean text
                cleaned_text = self._clean_text(full_text)

                # Extract metadata
                metadata = {
                    "page_count": num_pages,
                    "word_count": len(cleaned_text.split()),
                    "char_count": len(cleaned_text),
                    "has_images": any(
                        page.images for page in pdf.pages
                    ),
                }

                return cleaned_text, metadata

        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")

    async def parse_text(self, text: str) -> Tuple[str, dict]:
        """
        Process manually entered text.

        Args:
            text: Raw text input

        Returns:
            Tuple of (cleaned_text, metadata)
        """
        cleaned_text = self._clean_text(text)

        metadata = {
            "page_count": 1,
            "word_count": len(cleaned_text.split()),
            "char_count": len(cleaned_text),
            "has_images": False,
            "source": "manual_input",
        }

        return cleaned_text, metadata

    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text.

        Args:
            text: Raw extracted text

        Returns:
            Cleaned text
        """
        if not text:
            return ""

        # Remove excessive whitespace
        text = re.sub(r"\s+", " ", text)

        # Remove excessive newlines but preserve paragraph structure
        text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

        # Fix common PDF extraction issues
        text = text.replace("\x00", "")  # Remove null bytes
        text = text.replace("•", "- ")  # Normalize bullets

        # Remove page numbers (common patterns)
        text = re.sub(r"\n\s*\d+\s*\n", "\n", text)

        return text.strip()

    def extract_sections(self, text: str) -> dict:
        """
        Attempt to identify common CV sections.

        Args:
            text: Cleaned CV text

        Returns:
            Dictionary with section names as keys
        """
        sections = {
            "header": "",
            "summary": "",
            "experience": "",
            "education": "",
            "skills": "",
            "certifications": "",
            "other": "",
        }

        # Common section headers in multiple languages
        section_patterns = {
            "summary": r"(?i)(resumen|summary|perfil|profile|objetivo|objective|about)[:\s\n]",
            "experience": r"(?i)(experiencia|experience|empleo|employment|trabajo|work history)[:\s\n]",
            "education": r"(?i)(educación|education|formación|academic|estudios)[:\s\n]",
            "skills": r"(?i)(habilidades|skills|competencias|competencies|tecnologías)[:\s\n]",
            "certifications": r"(?i)(certificaciones|certifications|cursos|courses)[:\s\n]",
        }

        # Simple heuristic: find section starts
        import re

        section_starts = {}
        for section, pattern in section_patterns.items():
            matches = list(re.finditer(pattern, text))
            if matches:
                section_starts[section] = matches[0].start()

        # Sort by position
        sorted_sections = sorted(section_starts.items(), key=lambda x: x[1])

        # First section before any identified section is likely header
        if sorted_sections:
            first_section_start = sorted_sections[0][1]
            sections["header"] = text[:first_section_start].strip()

        # Extract content between sections
        for i, (section_name, start_pos) in enumerate(sorted_sections):
            if i + 1 < len(sorted_sections):
                end_pos = sorted_sections[i + 1][1]
            else:
                end_pos = len(text)

            sections[section_name] = text[start_pos:end_pos].strip()

        return sections
