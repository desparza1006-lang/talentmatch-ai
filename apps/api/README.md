# TalentMatch AI - Backend API

FastAPI-based backend for AI-powered CV analysis and job matching.

## Features

- 📄 **PDF Parsing**: Extract text from CV PDFs using pdfplumber
- 🔍 **Information Extraction**: Automatically detect skills, experience, education
- 🧠 **Semantic Matching**: Use embeddings (Ollama) for accurate CV-Job comparison
- 📊 **Scoring Algorithm**: Weighted multi-factor compatibility calculation
- 💡 **AI Insights**: LLM-powered recommendations and gap analysis

## Quick Start

### Prerequisites

- Python 3.11+
- Ollama installed locally ([ollama.com](https://ollama.com))

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup Ollama models
ollama pull nomic-embed-text
ollama pull llama3.2:3b

# Run the API
uvicorn app.main:app --reload --port 8000
```

### Environment Variables

Create a `.env` file:

```env
DEBUG=true
DATABASE_URL=sqlite+aiosqlite:///./talentmatch.db
OLLAMA_BASE_URL=http://localhost:11434
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## Project Structure

```
app/
├── main.py           # FastAPI entry point
├── config.py         # Settings management
├── routers/          # API endpoints
├── services/         # Business logic
├── schemas/          # Pydantic models
├── db/               # Database models
└── utils/            # Utilities
```

## Development

```bash
# Format code
black app/
isort app/

# Type checking
mypy app/

# Run tests
pytest
```

## Architecture

1. **PDF Upload** → Parser extracts text
2. **Extraction** → Regex/heuristics extract structured data
3. **Embeddings** → Ollama generates semantic vectors
4. **Matching** → Cosine similarity + weighted scoring
5. **LLM Enhancement** → (Optional) Additional insights
