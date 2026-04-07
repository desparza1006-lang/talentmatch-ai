"""Information extraction service using regex and heuristics."""

import re
from datetime import datetime
from typing import Dict, List, Optional

from app.schemas.cv import (
    CVData,
    Education,
    Experience,
    PersonalInfo,
    SkillSet,
)


class InformationExtractor:
    """Extract structured information from CV text."""

    # Common technical skills
    TECH_SKILLS = {
        # Programming languages
        "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust",
        "ruby", "php", "swift", "kotlin", "scala", "r", "matlab",
        # Web
        "html", "css", "react", "angular", "vue", "svelte", "next.js", "nuxt",
        "node.js", "express", "django", "flask", "fastapi", "spring",
        # Databases
        "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
        "firebase", "supabase", "dynamodb", "cassandra",
        # Cloud/DevOps
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
        "jenkins", "github actions", "gitlab ci", "circleci", "travis",
        # Data/ML
        "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
        "keras", "spark", "hadoop", "tableau", "powerbi",
        # Mobile
        "react native", "flutter", "ionic", "android", "ios",
        # Tools
        "git", "github", "gitlab", "bitbucket", "jira", "confluence",
        "figma", "sketch", "adobe xd", "notion", "slack",
    }

    # Common soft skills
    SOFT_SKILLS = {
        "liderazgo", "leadership", "comunicación", "communication",
        "trabajo en equipo", "teamwork", "proactivo", "proactive",
        "resolución de problemas", "problem solving", "adaptabilidad",
        "adaptability", "creatividad", "creativity", "pensamiento crítico",
        "critical thinking", "gestión del tiempo", "time management",
        "negociación", "negotiation", "empatía", "empathy",
        "orientación a resultados", "result-oriented", "autonomía",
        "self-motivated", "aprendizaje continuo", "continuous learning",
    }

    def extract(self, text: str, sections: Optional[Dict[str, str]] = None) -> CVData:
        """
        Extract all structured information from CV text.

        Args:
            text: Full CV text
            sections: Optional pre-extracted sections

        Returns:
            Structured CVData object
        """
        if sections is None:
            from app.services.parser import CVParser

            parser = CVParser()
            sections = parser.extract_sections(text)

        personal_info = self._extract_personal_info(text, sections.get("header", ""))
        skills = self._extract_skills(text)
        experience = self._extract_experience(sections.get("experience", text))
        education = self._extract_education(sections.get("education", text))
        summary = self._extract_summary(sections.get("summary", ""))

        return CVData(
            personal_info=personal_info,
            summary=summary,
            skills=skills,
            experience=experience,
            education=education,
            raw_text=text,
        )

    def _extract_personal_info(self, text: str, header: str) -> PersonalInfo:
        """Extract personal information."""
        search_text = header or text[:2000]  # Search in first 2000 chars if no header

        # Email pattern
        email_match = re.search(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            search_text,
        )
        email = email_match.group(0) if email_match else None

        # Phone pattern (Spanish and international)
        phone_patterns = [
            r"\+\d{1,3}[\s.-]?\d{1,4}[\s.-]?\d{1,4}[\s.-]?\d{1,4}",
            r"\(?\d{2,3}\)?[\s.-]?\d{3}[\s.-]?\d{2}[\s.-]?\d{2}",
        ]
        phone = None
        for pattern in phone_patterns:
            match = re.search(pattern, search_text)
            if match:
                phone = match.group(0)
                break

        # LinkedIn
        linkedin_match = re.search(
            r"linkedin\.com/in/[a-zA-Z0-9-]+", search_text, re.IGNORECASE
        )
        linkedin = f"https://{linkedin_match.group(0)}" if linkedin_match else None

        # Website/Portfolio
        website_match = re.search(
            r"(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.(?:com|dev|io|github\.io)",
            search_text,
            re.IGNORECASE,
        )
        portfolio = website_match.group(0) if website_match else None

        # Name - heuristic: first 1-2 capitalized words at the beginning
        name = None
        lines = search_text.strip().split("\n")
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            # Skip if it looks like email or link
            if "@" in line or "http" in line.lower():
                continue
            # Look for 1-2 capitalized words
            name_match = re.match(r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})$", line)
            if name_match and len(line) > 3:
                name = line
                break

        # Location
        location_match = re.search(
            r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*,\s*(?:España|Spain|Argentina|Mexico|Chile|Colombia|Peru|USA|UK|Remote|Remoto))",
            search_text,
        )
        location = location_match.group(1) if location_match else None

        return PersonalInfo(
            name=name,
            email=email,
            phone=phone,
            location=location,
            linkedin=linkedin,
            portfolio=portfolio,
        )

    def _extract_skills(self, text: str) -> SkillSet:
        """Extract skills from text."""
        text_lower = text.lower()
        words = set(re.findall(r"\b\w+(?:\+\+?|\.js|\.py)?\b", text_lower))

        technical = []
        soft = []
        tools = []

        for skill in self.TECH_SKILLS:
            if skill in text_lower or skill.replace(" ", "") in text_lower.replace(
                " ", ""):
                # Categorize
                if skill in {
                    "docker",
                    "kubernetes",
                    "git",
                    "github",
                    "jira",
                    "figma",
                }:
                    tools.append(skill)
                else:
                    technical.append(skill)

        for skill in self.SOFT_SKILLS:
            if skill in text_lower:
                soft.append(skill)

        # Languages
        languages = self._extract_languages(text)

        return SkillSet(
            technical=list(set(technical)),
            soft=list(set(soft)),
            tools=list(set(tools)),
            languages=languages,
        )

    def _extract_languages(self, text: str) -> List[dict]:
        """Extract language proficiencies."""
        languages = []
        text_lower = text.lower()

        # Common language patterns
        lang_patterns = {
            "español": "native",
            "spanish": "native",
            "inglés": "intermediate",
            "english": "intermediate",
            "francés": "basic",
            "french": "basic",
            "alemán": "basic",
            "german": "basic",
            "portugués": "intermediate",
            "portuguese": "intermediate",
            "italiano": "basic",
            "italian": "basic",
        }

        proficiency_keywords = {
            "nativo": "native",
            "native": "native",
            "bilingüe": "bilingual",
            "bilingual": "bilingual",
            "avanzado": "advanced",
            "advanced": "advanced",
            "c1": "advanced",
            "c2": "advanced",
            "intermedio": "intermediate",
            "intermediate": "intermediate",
            "b1": "intermediate",
            "b2": "intermediate",
            "básico": "basic",
            "basico": "basic",
            "basic": "basic",
            "a1": "basic",
            "a2": "basic",
        }

        for lang, default_level in lang_patterns.items():
            if lang in text_lower:
                level = default_level
                # Try to find proficiency level nearby
                lang_pos = text_lower.find(lang)
                context = text_lower[max(0, lang_pos - 50) : lang_pos + 50]
                for keyword, prof_level in proficiency_keywords.items():
                    if keyword in context:
                        level = prof_level
                        break

                languages.append({"name": lang.capitalize(), "level": level})

        return languages

    def _extract_experience(self, text: str) -> List[Experience]:
        """Extract work experience entries."""
        experiences = []

        # Split by common delimiters
        entries = re.split(r"\n(?=[A-Z][^a-z]*\n|[•\-\*])", text)

        for entry in entries:
            if len(entry.strip()) < 20:
                continue

            # Date patterns
            date_patterns = [
                r"((?:Ene|Feb|Mar|Abr|May|Jun|Jul|Ago|Sep|Oct|Nov|Dic|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\w\.]*\s+\d{4})\s*[-–]\s*((?:Ene|Feb|Mar|Abr|May|Jun|Jul|Ago|Sep|Oct|Nov|Dic|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\w\.]*\s+\d{4}|actual|present|now)",
                r"(\d{2}/\d{4})\s*[-–]\s*(\d{2}/\d{4}|actual|present|now)",
                r"(\d{4})\s*[-–]\s*(\d{4}|actual|present|now)",
            ]

            start_date = None
            end_date = None
            is_current = False

            for pattern in date_patterns:
                match = re.search(pattern, entry, re.IGNORECASE)
                if match:
                    start_date = match.group(1)
                    end_date = match.group(2)
                    is_current = end_date.lower() in ["actual", "present", "now"]
                    break

            # Company and title heuristics
            lines = entry.strip().split("\n")
            company = None
            title = None

            if lines:
                # First substantial line often contains company/title
                first_line = lines[0]
                if "@" in first_line:
                    parts = first_line.split("@")
                    title = parts[0].strip()
                    company = parts[1].strip()
                elif " - " in first_line or " | " in first_line:
                    parts = re.split(r"\s*[-|]\s*", first_line)
                    if len(parts) >= 2:
                        title = parts[0].strip()
                        company = parts[1].strip()

            if company or title or start_date:
                experiences.append(
                    Experience(
                        company=company,
                        title=title,
                        start_date=start_date,
                        end_date=end_date,
                        is_current=is_current,
                        description=entry.strip(),
                    )
                )

        return experiences[:10]  # Limit to top 10 experiences

    def _extract_education(self, text: str) -> List[Education]:
        """Extract education entries."""
        education = []

        # Common degree keywords
        degree_keywords = [
            "licenciatura",
            "licenciado",
            "ingeniería",
            "ingeniero",
            "grado",
            "degree",
            "bachelor",
            "master",
            "mba",
            "phd",
            "doctorado",
            "técnico",
            "tecnico",
            "fp",
            "ciclo formativo",
        ]

        entries = re.split(r"\n(?=[A-Z][^a-z]*\n|[•\-\*])", text)

        for entry in entries:
            entry_lower = entry.lower()

            # Check if it looks like education
            if not any(kw in entry_lower for kw in degree_keywords + ["universidad", "university", "instituto", "school"]):
                continue

            # Extract year
            year_match = re.search(r"\b(20\d{2}|19\d{2})\b", entry)
            year = int(year_match.group(1)) if year_match else None

            # Institution heuristic: capitalized words before degree
            institution = None
            degree = None
            field = None

            lines = entry.strip().split("\n")
            if lines:
                # First line often has institution and/or degree
                first_line = lines[0]
                inst_match = re.search(r"(?:Universidad|University|Instituto|School)\s+de\s+([\w\s]+)", first_line, re.IGNORECASE)
                if inst_match:
                    institution = inst_match.group(0)

            education.append(
                Education(
                    institution=institution,
                    degree=degree,
                    field=field,
                    end_year=year,
                    description=entry.strip(),
                )
            )

        return education[:5]

    def _extract_summary(self, text: str) -> Optional[str]:
        """Extract professional summary."""
        if not text:
            return None

        # Clean up and limit length
        summary = text.strip()
        if len(summary) > 1000:
            summary = summary[:997] + "..."

        return summary if summary else None
