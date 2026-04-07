"""Text cleaning and normalization utilities."""

import re
import unicodedata


def normalize_text(text: str) -> str:
    """Normalize text by removing accents and standardizing case."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ASCII", "ignore").decode("ASCII")
    return text.lower().strip()


def remove_extra_whitespace(text: str) -> str:
    """Remove extra whitespace and normalize newlines."""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def extract_emails(text: str) -> list:
    """Extract email addresses from text."""
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return re.findall(pattern, text)


def extract_urls(text: str) -> list:
    """Extract URLs from text."""
    pattern = r"https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?"
    return re.findall(pattern, text)


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to max_length characters."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def detect_language(text: str) -> str:
    """Simple language detection based on common words."""
    text_lower = text.lower()

    spanish_words = {
        "el",
        "la",
        "de",
        "que",
        "y",
        "a",
        "en",
        "un",
        "ser",
        "se",
        "no",
        "haber",
        "por",
        "con",
        "su",
        "para",
        "como",
        "estar",
        "tener",
        "le",
        "lo",
        "pero",
        "más",
        "hacer",
    }
    english_words = {
        "the",
        "be",
        "to",
        "of",
        "and",
        "a",
        "in",
        "that",
        "have",
        "i",
        "it",
        "for",
        "not",
        "on",
        "with",
        "he",
        "as",
        "you",
        "do",
        "at",
        "this",
        "but",
        "his",
        "by",
        "from",
    }

    spanish_count = sum(1 for word in spanish_words if word in text_lower)
    english_count = sum(1 for word in english_words if word in text_lower)

    if spanish_count > english_count:
        return "es"
    elif english_count > spanish_count:
        return "en"
    return "unknown"
