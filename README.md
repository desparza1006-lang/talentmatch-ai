# TalentMatch AI 🎯

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.12+-blue)
![Node](https://img.shields.io/badge/node-18+-green)

> Análisis inteligente de CVs con IA local. Compara tu perfil con ofertas laborales y obtén insights personalizados sobre tu compatibilidad, **todo de forma privada sin enviar datos a la nube**.

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Objetivo del Sistema](#-objetivo-del-sistema)
- [Características Principales](#-características-principales)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Ejecución Local](#-ejecución-local)
- [Uso con Docker](#-uso-con-docker)
- [Servicios y Dependencias](#-servicios-y-dependencias)
- [Limitaciones y Notas](#-limitaciones-y-notas)
- [Solución de Problemas](#-solución-de-problemas)
- [Estado del Proyecto](#-estado-del-proyecto)

---

## 📝 Descripción General

**TalentMatch AI** es una aplicación full-stack que utiliza inteligencia artificial local para analizar currículums y compararlos con descripciones de trabajo. El sistema extrae información estructurada de CVs en PDF, genera embeddings semánticos usando modelos locales vía Ollama, y calcula un score de compatibilidad ponderado con análisis detallado de fortalezas, brechas y recomendaciones personalizadas.

### ¿Por qué TalentMatch AI?

| Ventaja | Descripción |
|---------|-------------|
| 🔒 **Privacidad total** | Todo el procesamiento es local, tus CVs nunca salen de tu computadora |
| 💰 **Sin costos** | No requiere API keys ni servicios en la nube |
| ⚡ **Rápido** | Procesamiento local sin latencia de red externa |
| 🎯 **Preciso** | Matching semántico con embeddings de 768 dimensiones |

---

## 🎯 Objetivo del Sistema

El objetivo principal es ayudar a candidatos a:

1. **Entender su compatibilidad** con una oferta laboral específica
2. **Identificar fortalezas** que resaltar en el proceso de selección
3. **Detectar brechas** de habilidades o experiencia
4. **Recibir recomendaciones** accionables para mejorar su perfil

---

## ✨ Características Principales

| Característica | Descripción |
|----------------|-------------|
| 📄 **Extracción de PDFs** | Parsea CVs en PDF y extrae texto estructurado usando `pdfplumber` |
| 🧠 **Matching Semántico** | Usa embeddings locales (Ollama + nomic-embed-text) para comparación precisa |
| 📊 **Score de Compatibilidad** | Algoritmo ponderado multi-factor: Skills 40%, Experiencia 30%, Educación 15%, General 15% |
| 💡 **Recomendaciones IA** | Sugerencias personalizadas generadas por LLM local (llama3.2:3b) |
| 🔒 **100% Privado** | Sin envío de datos a servicios externos |
| 🎨 **UI Moderna** | Interfaz limpia con Next.js 16 + Tailwind CSS 4 + shadcn/ui |

---

## 🛠️ Tecnologías Utilizadas

### Frontend (`apps/web/`)
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Next.js | 16.2.1 | Framework React con App Router |
| React | 19.2.4 | Biblioteca UI |
| TypeScript | 5.x | Tipado estático |
| Tailwind CSS | 4.x | Estilos utilitarios |
| Zustand | 5.x | Gestión de estado |
| shadcn/ui | 4.x | Componentes UI |
| Recharts | 3.x | Visualización de datos |

### Backend (`apps/api/`)
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| FastAPI | 0.115.0 | Framework web asíncrono |
| Python | 3.12+ | Lenguaje de programación |
| Pydantic | 2.9.2 | Validación de datos |
| SQLAlchemy | 2.0.36 | ORM async |
| aiosqlite | 0.20.0 | Base de datos SQLite async |
| Alembic | 1.14.0 | Migraciones de BD |

### Procesamiento de IA (Local)
| Tecnología | Modelo | Propósito |
|------------|--------|-----------|
| Ollama | latest | Plataforma para ejecutar modelos localmente |
| nomic-embed-text | - | Embeddings de 768 dimensiones |
| llama3.2:3b | - | LLM para generación de insights |

### Procesamiento de PDFs
- **pdfplumber** 0.11.4 - Extracción de texto de PDFs
- **pypdf** 5.1.0 - Manipulación de archivos PDF

---

## 📁 Estructura del Proyecto

```
talentmatch-ai/
├── apps/
│   ├── api/                     # Backend FastAPI
│   │   ├── app/
│   │   │   ├── routers/         # Endpoints API (cv, matching, analysis)
│   │   │   ├── services/        # Lógica de negocio (parser, extractor, matcher, embedder, llm)
│   │   │   ├── schemas/         # Modelos Pydantic
│   │   │   ├── db/              # Modelos y configuración de BD (SQLAlchemy + aiosqlite)
│   │   │   └── utils/           # Utilidades y constantes
│   │   ├── requirements.txt     # Dependencias Python
│   │   ├── .env.example         # Plantilla de variables de entorno
│   │   └── Dockerfile           # Configuración Docker
│   │
│   └── web/                     # Frontend Next.js
│       ├── app/                 # Páginas y layouts (App Router)
│       ├── components/          # Componentes React
│       ├── lib/                 # Utilidades y stores (Zustand)
│       ├── package.json         # Dependencias Node.js
│       └── .env.local.example   # Plantilla de variables de entorno
│
├── docs/
│   └── architecture.md          # Documentación de arquitectura
├── scripts/
│   └── setup.ps1               # Script de setup automático (Windows)
├── docker-compose.yml          # Orquestación Docker completa
├── railway.toml               # Configuración para Railway (deploy)
└── README.md                  # Este archivo
```

---

## 📋 Requisitos Previos

### Software Obligatorio

| Software | Versión | Descripción | Importancia |
|----------|---------|-------------|-------------|
| Python | 3.12+ | Recomendado 3.12 para estabilidad en Windows | ⚠️ Crítico |
| Node.js | 18+ | Incluye npm | ⚠️ Crítico |
| Ollama | latest | Motor de IA local | ⚠️ Crítico |

> ⚠️ **IMPORTANTE**: Se recomienda **Python 3.12** en lugar de 3.13 porque algunas librerías de procesamiento de PDF no tienen wheels precompilados para Windows + Python 3.13.

### Hardware Recomendado

| Recurso | Mínimo | Recomendado |
|---------|--------|-------------|
| RAM | 8GB | 16GB |
| Disco | 5GB libres | 10GB libres |
| CPU | Procesador moderno | Con soporte AVX2 |

> 💡 **Nota**: Los modelos de Ollama corren localmente y requieren recursos. La primera ejecución puede ser lenta mientras se cargan los modelos en memoria.

---

## 🚀 Instalación

### Paso 1: Instalar Ollama

1. Descarga e instala Ollama desde: https://ollama.com
2. Verifica la instalación:
   ```bash
   ollama --version
   ```

### Paso 2: Descargar Modelos de IA

```bash
ollama pull nomic-embed-text
ollama pull llama3.2:3b
```

### Paso 3: Clonar el Repositorio

```bash
git clone https://github.com/desparza1006-lang/talentmatch-ai.git
cd talentmatch-ai
```

### Paso 4: Configurar Backend

**Opción A: Python 3.12 (Recomendado para Windows)**

```powershell
# Navegar al directorio del backend
cd apps/api

# Eliminar entorno virtual anterior si existe
if (Test-Path "venv") { Remove-Item -Recurse -Force "venv" }

# Crear entorno virtual con Python 3.12
py -3.12 -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1        # Windows
# source venv/bin/activate          # macOS/Linux

# Actualizar pip e instalar dependencias
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Opción B: Python 3.13 (Temporal / Prueba)**

```powershell
cd apps/api
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Paso 5: Configurar Frontend

```powershell
# En otra terminal, navegar al frontend
cd apps/web

# Instalar dependencias
npm install
```

---

## ⚙️ Configuración

### Variables de Entorno - Backend

Crea un archivo `.env` en `apps/api/` copiando `.env.example`:

```bash
cd apps/api
copy .env.example .env    # Windows
cp .env.example .env      # macOS/Linux
```

**Contenido de `.env`:**

```env
# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=TalentMatch AI API
DEBUG=true

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]

# Database
DATABASE_URL=sqlite+aiosqlite:///./talentmatch.db

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
OLLAMA_LLM_MODEL=llama3.2:3b
OLLAMA_TIMEOUT=120

# Processing Limits
MAX_FILE_SIZE_MB=10
MAX_CV_PAGES=10
CHUNK_SIZE=512
CHUNK_OVERLAP=50
```

### Variables de Entorno - Frontend

Crea un archivo `.env.local` en `apps/web/` copiando `.env.local.example`:

```bash
cd apps/web
copy .env.local.example .env.local    # Windows
cp .env.local.example .env.local      # macOS/Linux
```

**Contenido de `.env.local`:**

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

## ▶️ Ejecución Local

> **⚠️ IMPORTANTE**: Frontend y Backend corren como **procesos separados**. Necesitarás **dos terminales**.

### Terminal 1 - Backend

```powershell
cd apps/api
.\venv\Scripts\Activate.ps1        # Windows
# source venv/bin/activate          # macOS/Linux

uvicorn app.main:app --reload --port 8000
```

- API disponible en: http://localhost:8000
- Documentación interactiva: http://localhost:8000/api/v1/docs

### Terminal 2 - Frontend

```powershell
cd apps/web
npm run dev
```

- Aplicación disponible en: http://localhost:3000

### Verificar que Ollama está corriendo

```bash
curl http://localhost:11434/api/tags
```

Si no responde, inicia Ollama manualmente:
```bash
ollama serve
```

---

## 🐳 Uso con Docker

Como alternativa, puedes ejecutar todo el stack con Docker Compose:

```bash
# En la raíz del proyecto
docker-compose up -d
```

Esto levantará:
| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| Ollama | 11434 | Motor de IA local |
| Backend | 8000 | API FastAPI |
| Frontend | 3000 | Aplicación Next.js |

```bash
# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

---

## 🔌 Servicios y Dependencias

### Diagrama de Arquitectura

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Next.js   │──────▶│   FastAPI   │──────▶│   Ollama    │
│  (Puerto    │◀──────│  (Puerto    │◀──────│  (Puerto    │
│   3000)     │      │   8000)     │      │   11434)    │
└─────────────┘      └──────┬──────┘      └─────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │   SQLite    │
                     │  (local)    │
                     └─────────────┘
```

### Dependencias Externas Requeridas

| Servicio | Puerto | Requerido | Descripción |
|----------|--------|-----------|-------------|
| Ollama | 11434 | ✅ Siempre | Motor de IA local para embeddings y LLM |
| Backend | 8000 | ✅ Siempre | API FastAPI |
| Frontend | 3000 | ✅ Siempre | Aplicación Next.js |

> ⚠️ **Sin Ollama, la aplicación NO funciona**. Es un requisito obligatorio.

---

## ⚠️ Limitaciones y Notas

### Limitaciones Conocidas

| Limitación | Detalle |
|------------|---------|
| **Procesamiento local** | Requiere recursos de tu máquina. Más lento que APIs en la nube |
| **Base de datos** | SQLite file-based. **No es para producción** con múltiples usuarios |
| **Sin autenticación** | Versión MVP sin sistema de usuarios ni persistencia de sesiones |
| **Extracción de PDFs** | Funciona mejor con PDFs de texto. **Imágenes escaneadas no son soportadas** |
| **Primer análisis lento** | Ollama debe cargar modelos en memoria la primera vez |

### Notas de Desarrollo

- **Frontend y Backend separados**: Cada uno tiene su propio `package.json` y `requirements.txt`
- **Variables de entorno obligatorias**: Sin ellas, la aplicación no se conecta correctamente
- **Ollama es imprescindible**: No hay fallback a servicios en la nube
- **SQLite local**: La base de datos se crea automáticamente en el primer arranque

---

## 🔧 Solución de Problemas

### Error "Ollama connection refused"

```bash
# Verificar si Ollama está corriendo
curl http://localhost:11434/api/tags

# Si no responde, iniciar manualmente
ollama serve
```

### Error de compilación en Windows (Python 3.13)

Algunas librerías no tienen wheels precompilados para Python 3.13 en Windows.

**Solución:** Usa Python 3.12
```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Error "Cannot find module" en Node.js

```powershell
cd apps/web
Remove-Item -Recurse -Force node_modules
npm install
```

### Error de dependencias de Python (Meson / numpy)

Este error ocurre con Python 3.13 en Windows porque faltan compiladores C/C++.

**Solución definitiva:**
1. Instala Python 3.12 desde https://www.python.org/downloads/release/python-3127/
2. Recrea el entorno virtual con `py -3.12 -m venv venv`
3. Reinstala dependencias

---

## 📊 Estado del Proyecto

### Versión Actual: 1.0.0 ✅

**Estado**: MVP Funcional - Listo para uso local

### Funcionalidades Implementadas ✅

- [x] Subida de CV en PDF
- [x] Input manual de texto
- [x] Extracción de información (nombre, skills, experiencia, educación)
- [x] Matching semántico con embeddings
- [x] Score de compatibilidad ponderado
- [x] Análisis de fortalezas y brechas
- [x] Recomendaciones personalizadas con LLM
- [x] UI moderna y responsive

### Roadmap Futuro

- [ ] Autenticación de usuarios
- [ ] Historial de análisis persistente
- [ ] Mejora de CV con LLM
- [ ] Consejos para entrevistas
- [ ] Integración con LinkedIn
- [ ] Migración a PostgreSQL para producción

---

## 🤝 Contribuir

Este es un proyecto de portfolio. Las contribuciones son bienvenidas:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Add: nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📝 Licencia

MIT License - Libre para uso personal y educativo.

---

<p align="center">
  Built with ❤️ using FastAPI, Next.js, and Ollama
</p>
