"""CV processing endpoints."""

import time
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas.cv import CVData
from app.schemas.responses import APIResponse
from app.services.parser import CVParser
from app.services.extractor import InformationExtractor

router = APIRouter(prefix="/cv")


@router.post("/upload", response_model=APIResponse[CVData])
async def upload_cv(
    file: UploadFile = File(..., description="PDF file to analyze"),
) -> APIResponse[CVData]:
    """
    Upload and parse a CV PDF file.

    Extracts structured information including personal info, skills,
    experience, and education.
    """
    start_time = time.time()

    # Validate file type
    if not file.content_type or not file.content_type.endswith("pdf"):
        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="File must be a PDF",
            )

    try:
        # Read file content
        content = await file.read()

        # Parse PDF
        parser = CVParser()
        text, metadata = await parser.parse_pdf(content)

        # Extract structured information
        extractor = InformationExtractor()
        sections = parser.extract_sections(text)
        cv_data = extractor.extract(text, sections)

        processing_time = int((time.time() - start_time) * 1000)

        return APIResponse(
            success=True,
            data=cv_data,
            message=f"CV processed successfully. {metadata.get('page_count', 0)} pages, {metadata.get('word_count', 0)} words.",
            processing_time_ms=processing_time,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process CV: {str(e)}",
        )


@router.post("/parse-text", response_model=APIResponse[CVData])
async def parse_cv_text(
    text: str = Form(..., description="CV text content"),
) -> APIResponse[CVData]:
    """
    Parse CV from manually entered text.

    Alternative to PDF upload for users who prefer to paste text directly.
    """
    start_time = time.time()

    if not text or len(text.strip()) < 50:
        raise HTTPException(
            status_code=400,
            detail="Text too short. Please provide at least 50 characters.",
        )

    try:
        # Parse text
        parser = CVParser()
        cleaned_text, metadata = await parser.parse_text(text)

        # Extract structured information
        extractor = InformationExtractor()
        sections = parser.extract_sections(cleaned_text)
        cv_data = extractor.extract(cleaned_text, sections)

        processing_time = int((time.time() - start_time) * 1000)

        return APIResponse(
            success=True,
            data=cv_data,
            message=f"Text processed successfully. {metadata.get('word_count', 0)} words extracted.",
            processing_time_ms=processing_time,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process text: {str(e)}",
        )
