# 🚀 TalentMatch AI - Guía Rápida de Inicio

## ✅ Requisitos Verificados

- **Python 3.12 recomendado** para mayor estabilidad en Windows (especialmente con librerías de NLP/data science).
- Si solo tienes **Python 3.13**, puedes probar el proyecto temporalmente después de quitar spaCy (ya hecho).
- ✅ Node.js v22.13.1 instalado
- ✅ Estructura de proyecto creada

## 📦 Instalación

### Paso 1: Instalar Ollama

1. Descarga Ollama desde: https://ollama.com
2. Instálalo y asegúrate de que esté corriendo:
```bash
ollama --version
```

### Paso 2: Descargar modelos de IA

```bash
ollama pull nomic-embed-text
ollama pull llama3.2:3b
```

### Paso 3: Configurar Backend (FastAPI)

#### Opción A: Python 3.12 (recomendado para Windows)

Si ya instalaste Python 3.12, usa estos comandos exactos en PowerShell:

```powershell
# Navegar al directorio del backend
cd apps/api

# Eliminar entorno virtual anterior si existe (IMPORTANTE)
if (Test-Path "venv") { Remove-Item -Recurse -Force "venv" }

# Crear entorno virtual con Python 3.12 explícitamente
py -3.12 -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo de configuración
copy .env.example .env
```

#### Opción B: Python 3.13 (temporal / prueba)

Si aún no has instalado Python 3.12 y quieres probar con tu 3.13 actual, ejecuta:

```powershell
# Navegar al directorio del backend
cd apps/api

# Eliminar entorno virtual anterior si existe (IMPORTANTE)
if (Test-Path "venv") { Remove-Item -Recurse -Force "venv" }

# Crear entorno virtual con Python 3.13
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias (ya sin spaCy)
pip install -r requirements.txt

# Crear archivo de configuración
copy .env.example .env
```

> ⚠️ **Nota sobre Python 3.13**: Algunas librerías de procesamiento de PDF o data science pueden seguir sin tener wheels precompiladas para Windows + Python 3.13. Si la instalación sigue fallando con errores de compilador (`cl`, `gcc`, `Meson`), instala **Python 3.12** y usa la Opción A.

### Paso 4: Configurar Frontend (Next.js)

```powershell
# En una nueva terminal, navegar al frontend
cd apps/web

# Instalar dependencias
npm install

# Crear archivo de configuración
copy .env.local.example .env.local
```

## ▶️ Ejecución

### Terminal 1: Backend

```powershell
cd apps/api
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

La API estará disponible en: http://localhost:8000

Documentación: http://localhost:8000/api/v1/docs

### Terminal 2: Frontend

```powershell
cd apps/web
npm run dev
```

La aplicación estará disponible en: http://localhost:3000

## 🧪 Probar la Aplicación

1. Abre http://localhost:3000 en tu navegador
2. Haz clic en "Comenzar gratis" o "Analizar CV"
3. Sube un PDF de CV o pega texto manualmente
4. Pega una descripción de trabajo
5. ¡Obtén tu análisis de compatibilidad!

## 📁 Estructura del Proyecto

```
talentmatch-ai/
├── apps/
│   ├── api/              # Backend FastAPI
│   │   ├── app/
│   │   │   ├── routers/      # Endpoints API
│   │   │   ├── services/     # Lógica de negocio
│   │   │   ├── schemas/      # Modelos Pydantic
│   │   │   └── ...
│   │   └── requirements.txt
│   └── web/              # Frontend Next.js
│       ├── app/              # Páginas
│       ├── components/       # Componentes React
│       └── ...
├── docs/
│   └── architecture.md   # Documentación de arquitectura
├── scripts/
│   └── setup.ps1         # Script de setup (Windows)
└── README.md
```

## 🔧 Solución de Problemas

### "Ollama connection refused"
Asegúrate de que Ollama esté corriendo:
```bash
# Verificar estado
curl http://localhost:11434/api/tags

# Si no responde, iniciar Ollama manualmente
ollama serve
```

### Error al instalar dependencias de Python (compiladores / Meson / numpy)
Este error ocurre principalmente con **Python 3.13 en Windows** porque algunas librerías no tienen binarios precompilados (wheels) y el sistema intenta compilarlas desde código fuente, pero no encuentra compiladores C/C++.

**Solución definitiva:**
1. Desinstala o deja de usar el entorno virtual con Python 3.13.
2. Instala **Python 3.12** desde https://www.python.org/downloads/release/python-3127/
3. Recrea el entorno virtual con `py -3.12 -m venv venv` (ver Opción A arriba).
4. Vuelve a ejecutar `pip install -r requirements.txt`.

### Error "Cannot find module"
```powershell
# Borrar node_modules y reinstalar
cd apps/web
Remove-Item -Recurse -Force node_modules
npm install
```

## 📚 Documentación Adicional

- [Arquitectura del Sistema](docs/architecture.md)
- [README Backend](apps/api/README.md)
- [README Frontend](apps/web/README.md)

## 🎯 Características Implementadas

### MVP (Versión Actual)
- ✅ Subida de CV en PDF
- ✅ Input manual de texto
- ✅ Extracción de información (nombre, skills, experiencia, educación)
- ✅ Matching semántico con embeddings
- ✅ Score de compatibilidad ponderado
- ✅ Análisis de fortalezas y brechas
- ✅ Recomendaciones personalizadas
- ✅ UI moderna y responsive

### Próximas Versiones
- [ ] Autenticación de usuarios
- [ ] Historial de análisis persistente
- [ ] Mejora de CV con LLM
- [ ] Consejos para entrevistas
- [ ] Integración con LinkedIn

## 💡 Tips

1. **Para mejores resultados**, asegúrate de que tu CV tenga:
   - Información de contacto clara
   - Secciones bien definidas (Experiencia, Educación, Skills)
   - Texto seleccionable (no imágenes)

2. **Privacidad**: Todo el procesamiento es local. Los datos no salen de tu computadora.

3. **Rendimiento**: La primera ejecución puede ser lenta mientras Ollama carga los modelos.

---

¿Preguntas? Revisa la documentación o ejecuta el script de setup automático:
```powershell
.\scripts\setup.ps1
```
