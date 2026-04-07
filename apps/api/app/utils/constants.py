"""Application constants."""

# Supported file types
SUPPORTED_MIME_TYPES = {
    "application/pdf": ".pdf",
}

# Maximum content lengths
MAX_TEXT_LENGTH = 50000  # characters
MAX_SUMMARY_LENGTH = 2000  # characters
MAX_JOB_DESC_LENGTH = 10000  # characters

# Section headers (for parsing)
SECTION_HEADERS = {
    "experience": [
        "experience",
        "work experience",
        "employment history",
        "professional experience",
        "experiencia",
        "experiencia laboral",
        "experiencia profesional",
        "empleo",
        "trabajo",
    ],
    "education": [
        "education",
        "academic background",
        "qualifications",
        "educación",
        "formación",
        "estudios",
        "académico",
    ],
    "skills": [
        "skills",
        "technical skills",
        "competencies",
        "habilidades",
        "competencias",
        "conocimientos",
        "tecnologías",
    ],
    "summary": [
        "summary",
        "professional summary",
        "profile",
        "objective",
        "resumen",
        "perfil",
        "objetivo",
        "about",
        "sobre mí",
    ],
    "certifications": [
        "certifications",
        "certificates",
        "certificaciones",
        "certificados",
        "cursos",
        "courses",
    ],
}

# Common job titles for extraction
COMMON_JOB_TITLES = [
    "software engineer",
    "developer",
    "programmer",
    "analyst",
    "manager",
    "director",
    "consultant",
    "architect",
    "lead",
    "senior",
    "junior",
    "intern",
    "trainee",
    "freelance",
    "contractor",
]

# Score thresholds
MATCH_THRESHOLDS = {
    "excellent": 80,
    "good": 60,
    "moderate": 40,
    "poor": 20,
}
