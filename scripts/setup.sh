#!/bin/bash

# TalentMatch AI - Setup Script for macOS/Linux
# Run: chmod +x scripts/setup.sh && ./scripts/setup.sh

set -e

echo "🚀 TalentMatch AI Setup"
echo "======================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python not found. Please install Python 3.11+${NC}"
    exit 1
fi

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js found: $NODE_VERSION${NC}"
else
    echo -e "${RED}✗ Node.js not found. Please install Node.js 18+${NC}"
    exit 1
fi

# Check Ollama
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Ollama is running${NC}"
else
    echo -e "${RED}✗ Ollama not detected. Please:${NC}"
    echo -e "${YELLOW}  1. Install Ollama from https://ollama.com${NC}"
    echo -e "${YELLOW}  2. Start Ollama${NC}"
    echo -e "${YELLOW}  3. Run this script again${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Setting up backend...${NC}"

# Setup backend
cd "$(dirname "$0")/../apps/api"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${CYAN}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${CYAN}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${CYAN}Installing Python dependencies...${NC}"
pip install -r requirements.txt

echo ""
echo -e "${YELLOW}Setting up frontend...${NC}"

# Setup frontend
cd "$(dirname "$0")/../apps/web"

# Install dependencies
echo -e "${CYAN}Installing Node.js dependencies...${NC}"
npm install

echo ""
echo -e "${YELLOW}Pulling Ollama models...${NC}"

# Pull Ollama models
for model in nomic-embed-text llama3.2:3b; do
    echo -e "${CYAN}Pulling $model...${NC}"
    ollama pull $model
done

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo -e "${CYAN}To start the application:${NC}"
echo ""
echo -e "1. Start the backend:${NC}"
echo -e "   ${YELLOW}cd apps/api${NC}"
echo -e "   ${YELLOW}source venv/bin/activate${NC}"
echo -e "   ${YELLOW}uvicorn app.main:app --reload --port 8000${NC}"
echo ""
echo -e "2. Start the frontend (in a new terminal):${NC}"
echo -e "   ${YELLOW}cd apps/web${NC}"
echo -e "   ${YELLOW}npm run dev${NC}"
echo ""
echo -e "3. Open http://localhost:3000 in your browser${NC}"
