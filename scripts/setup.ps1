# TalentMatch AI - Setup Script for Windows
# Run this script to set up the development environment

$ErrorActionPreference = "Stop"

Write-Host "🚀 TalentMatch AI Setup" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

# Check Python
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check Node.js
$nodeVersion = node --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Node.js not found. Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

# Check Ollama
try {
    $ollamaResponse = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method GET -ErrorAction Stop
    Write-Host "✓ Ollama is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Ollama not detected. Please:" -ForegroundColor Red
    Write-Host "  1. Install Ollama from https://ollama.com" -ForegroundColor Yellow
    Write-Host "  2. Start Ollama" -ForegroundColor Yellow
    Write-Host "  3. Run this script again" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Setting up backend..." -ForegroundColor Yellow

# Setup backend
Set-Location -Path "$PSScriptRoot\..\apps\api"

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Cyan
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

Write-Host ""
Write-Host "Setting up frontend..." -ForegroundColor Yellow

# Setup frontend
Set-Location -Path "$PSScriptRoot\..\apps\web"

# Install dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Cyan
npm install

Write-Host ""
Write-Host "Pulling Ollama models..." -ForegroundColor Yellow

# Pull Ollama models
$models = @("nomic-embed-text", "llama3.2:3b")
foreach ($model in $models) {
    Write-Host "Pulling $model..." -ForegroundColor Cyan
    ollama pull $model
}

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the application:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Start the backend:" -ForegroundColor White
Write-Host "   cd apps\api" -ForegroundColor Yellow
Write-Host "   .\venv\Scripts\activate" -ForegroundColor Yellow
Write-Host "   uvicorn app.main:app --reload --port 8000" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Start the frontend (in a new terminal):" -ForegroundColor White
Write-Host "   cd apps\web" -ForegroundColor Yellow
Write-Host "   npm run dev" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Open http://localhost:3000 in your browser" -ForegroundColor White
