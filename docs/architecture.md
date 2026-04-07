# TalentMatch AI - Architecture Documentation

## System Overview

TalentMatch AI is a full-stack application for AI-powered CV analysis and job matching. The system extracts information from CVs, compares them with job descriptions using semantic embeddings, and provides actionable insights.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Next.js 14 (App Router)                                │   │
│  │  - React Server Components                             │   │
│  │  - Client-side state (Zustand)                         │   │
│  │  - File upload (react-dropzone)                        │   │
│  │  - UI Components (shadcn/ui + Tailwind)               │   │
│  └─────────────────────────────────────────────────────────┘   │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTP/REST (JSON)
┌──────────────────────────────▼──────────────────────────────────┐
│                         API LAYER                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  FastAPI                                                │   │
│  │  - Async request handling                              │   │
│  │  - Pydantic validation                                 │   │
│  │  - Auto-generated OpenAPI docs                         │   │
│  └─────────────────────────────────────────────────────────┘   │
└──────────────────────────────┬──────────────────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
┌─────────▼─────────┐ ┌───────▼────────┐ ┌────────▼────────┐
│  PROCESSING       │ │   EMBEDDINGS   │ │    LLM          │
│  SERVICES         │ │                │ │    SERVICE      │
│                   │ │   Ollama       │ │                 │
│  - PDF Parser     │ │                │ │   Ollama        │
│  - Info Extractor │ │   nomic-embed  │ │                 │
│  - Matcher        │ │                │ │   llama3.2:3b   │
└───────────────────┘ └────────────────┘ └─────────────────┘
          │
┌─────────▼─────────┐
│   DATABASE        │
│                   │
│   SQLite          │
│   (MVP)           │
│                   │
│   → PostgreSQL    │
│     (Future)      │
└───────────────────┘
```

## Data Flow

### 1. CV Upload Flow

```
User uploads PDF
       │
       ▼
┌─────────────┐
│ PDF Parser  │── pdfplumber ──► text extraction
└─────────────┘
       │
       ▼
┌─────────────────┐
│ Info Extractor  │── regex/heuristics ──► structured data
└─────────────────┘
       │
       ▼
┌─────────────┐
│   Response  │── CVData (JSON)
└─────────────┘
```

### 2. Matching Flow

```
CV Data + Job Data
       │
       ▼
┌─────────────┐
│  Embedder   │──► section texts prepared
└─────────────┘
       │
       ▼
┌─────────────┐
│   Ollama    │──► embeddings generated (768 dims)
└─────────────┘
       │
       ▼
┌─────────────┐
│   Matcher   │──► cosine similarity calculation
└─────────────┘
       │
       ▼
┌─────────────┐
│   Scoring   │──► weighted aggregation
└─────────────┘
       │
       ▼
┌─────────────┐
│  Analysis   │──► strengths, gaps, recommendations
└─────────────┘
```

## Component Details

### PDF Parser (`services/parser.py`)

**Responsibility**: Extract text from PDF files

**Process**:
1. Validate file size and page count
2. Use pdfplumber to extract text
3. Clean and normalize text
4. Identify sections using regex patterns

**Output**: Clean text + metadata + sections

### Information Extractor (`services/extractor.py`)

**Responsibility**: Extract structured data from text

**Methods**:
- Email/phone extraction using regex
- Name extraction (heuristic: first capitalized words)
- Skill extraction (keyword matching against predefined lists)
- Experience parsing (date patterns, company/title heuristics)
- Education extraction (degree keywords, year patterns)

**Note**: This is rule-based for the MVP. Future versions could use NER models.

### Embedder (`services/embedder.py`)

**Responsibility**: Generate semantic embeddings

**Model**: `nomic-embed-text` via Ollama
- 768-dimensional embeddings
- Optimized for semantic similarity
- Runs locally (privacy, no API costs)

**Process**:
1. Prepare text for each section (skills, experience, education, full)
2. Send to Ollama `/api/embeddings` endpoint
3. Return embedding vectors

### Matcher (`services/matcher.py`)

**Responsibility**: Calculate compatibility scores

**Algorithm**:
```python
# Section similarities (cosine)
skills_sim = cosine(cv_skills_emb, job_skills_emb)
exp_sim = cosine(cv_exp_emb, job_exp_emb)
edu_sim = cosine(cv_edu_emb, job_edu_emb)
overall_sim = cosine(cv_full_emb, job_full_emb)

# Weighted final score
final_score = (
    skills_sim * 0.40 +
    exp_sim * 0.30 +
    edu_sim * 0.15 +
    overall_sim * 0.15
) * 100
```

### LLM Service (`services/llm_service.py`)

**Responsibility**: Generate natural language insights

**Model**: `llama3.2:3b` via Ollama
- Lightweight (3B parameters)
- Runs on CPU
- Good for text generation tasks

**Uses**:
- Gap analysis narrative
- CV improvement suggestions
- Interview preparation tips

## Database Schema

### MVP (SQLite)

```sql
CREATE TABLE analyses (
    id TEXT PRIMARY KEY,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    
    -- CV
    cv_filename TEXT,
    cv_raw_text TEXT,
    cv_structured JSON,
    
    -- Job
    job_title TEXT,
    job_company TEXT,
    job_description TEXT,
    job_structured JSON,
    
    -- Results
    match_score FLOAT,
    match_details JSON,
    strengths JSON,
    gaps JSON,
    recommendations JSON,
    
    -- Metadata
    analysis_version TEXT,
    processing_time_ms INT
);
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/cv/upload` | Upload PDF CV |
| POST | `/api/v1/cv/parse-text` | Parse manual text input |
| POST | `/api/v1/matching/analyze` | Full CV-Job analysis |
| POST | `/api/v1/matching/quick-score` | Quick compatibility score |
| GET | `/api/v1/health` | Health check |

## Security Considerations

1. **Data Privacy**: All processing is local (Ollama)
2. **File Validation**: Size limits, MIME type checking
3. **Input Sanitization**: Text length limits
4. **CORS**: Configured for specific origins

## Performance Optimizations

1. **Async Processing**: FastAPI async handlers
2. **Connection Pooling**: HTTP client reuse for Ollama
3. **Caching**: Embeddings could be cached (future)
4. **Chunking**: Text split into manageable chunks

## Scaling Considerations

### Current (MVP)
- Single instance
- SQLite database
- Local Ollama

### Future (V2+)
- PostgreSQL with connection pooling
- Redis for caching
- Load balancer for API
- Separate Ollama instances or move to GPU

## Technology Choices

### Why FastAPI?
- Native async support
- Automatic API documentation
- Pydantic validation
- Python ecosystem for NLP/ML

### Why Ollama (Local LLM)?
- No API costs
- Data privacy (CVs have PII)
- No rate limits
- Works offline

### Why Next.js?
- React Server Components
- API routes for proxy
- Image optimization
- Easy deployment

### Why SQLite (MVP)?
- Zero configuration
- File-based (easy backup)
- Sufficient for single-user scenarios
- Easy migration path to PostgreSQL
