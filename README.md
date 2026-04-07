# TalentMatch AI 🎯

Análisis inteligente de CVs con IA local. Compara tu perfil con ofertas laborales y obtén insights personalizados sobre tu compatibilidad.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Node](https://img.shields.io/badge/node-18+-green)

## ✨ Características

- 📄 **Extracción Inteligente**: Parsea PDFs y extrae información estructurada
- 🧠 **Matching Semántico**: Usa embeddings locales (Ollama) para comparación precisa
- 📊 **Score de Compatibilidad**: Algoritmo ponderado multi-factor
- 💡 **Recomendaciones IA**: Sugerencias personalizadas para mejorar tu CV
- 🔒 **Privacidad Primero**: Todo el procesamiento es local, sin enviar datos a la nube
- 🎨 **UI Moderna**: Interfaz limpia y profesional con Next.js + Tailwind

## 🏗️ Arquitectura

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Next.js   │──────▶│   FastAPI   │──────▶│   Ollama    │
│  (Frontend) │◀──────│  (Backend)  │◀──────│  (Embeddings│
└─────────────┘      └─────────────┘      └─────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │   SQLite    │
                     │  (Storage)  │
                     └─────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12
- Node.js 18+
- [Ollama](https://ollama.com) installed

### Setup

1. **Clone and enter the project:**
```bash
cd talentmatch-ai
```

2. **Setup Ollama models:**
```bash
ollama pull nomic-embed-text
ollama pull llama3.2:3b
```

3. **Start the backend:**
```bash
cd apps/api

# Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload --port 8000
```

4. **Start the frontend:**
```bash
cd apps/web
npm install
npm run dev
```

5. **Open** [http://localhost:3000](http://localhost:3000)

## 📁 Project Structure

```
talentmatch-ai/
├── apps/
│   ├── api/              # FastAPI backend
│   │   ├── app/
│   │   │   ├── routers/  # API endpoints
│   │   │   ├── services/ # Business logic
│   │   │   ├── schemas/  # Pydantic models
│   │   │   └── ...
│   │   └── requirements.txt
│   └── web/              # Next.js frontend
│       ├── app/          # Pages
│       ├── components/   # React components
│       └── ...
├── docs/                 # Documentation
├── scripts/              # Utility scripts
└── README.md
```

## 🔧 Configuration

### Backend (.env)
```env
DEBUG=true
DATABASE_URL=sqlite+aiosqlite:///./talentmatch.db
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
OLLAMA_LLM_MODEL=llama3.2:3b
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## 📊 Algorithm Overview

The matching algorithm uses a weighted multi-factor approach:

| Factor | Weight | Description |
|--------|--------|-------------|
| Skills | 40% | Technical skills comparison using embeddings |
| Experience | 30% | Work experience relevance |
| Education | 15% | Academic background fit |
| Overall | 15% | General profile alignment |

**Cosine Similarity** is used to compare embeddings and calculate section scores.

## 🛣️ Roadmap

- [x] MVP: Basic CV upload and matching
- [ ] V1: User accounts and history
- [ ] V2: LLM-powered CV improvements
- [ ] V3: Interview preparation tips
- [ ] V4: LinkedIn integration

## 🤝 Contributing

This is a portfolio project, but contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - feel free to use this project for your own portfolio or learning.

---

Built with ❤️ using FastAPI, Next.js, and Ollama.
