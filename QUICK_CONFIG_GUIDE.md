# 🚀 Quick Configuration Guide

## ⚡ Change Ollama Model in 30 Seconds

### 1. Copy Configuration Template
```bash
cd backend
cp env.example .env
```

### 2. Edit Configuration
Open `.env` file and change the model:

```bash
# Change this line:
OLLAMA__MODEL_NAME=deepseek-r1:1.5b

# To your preferred model:
OLLAMA__MODEL_NAME=llama3.1:8b
```

### 3. Restart the Server
```bash
# Stop current server (Ctrl+C)
# Then restart:
source ./venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 3000
```

**Done!** Your new model is now active.

## 🎯 Quick Model Recommendations

| Use Case | Model | Why |
|----------|-------|-----|
| **Fast Development** | `deepseek-r1:1.5b` | Fastest responses |
| **Production Quality** | `llama3.1:8b` | Best balance of speed/quality |
| **Technical Analysis** | `codellama:13b` | Best for complex reasoning |
| **Resource Limited** | `mistral:7b` | Good quality, moderate speed |

## 🎨 Quick Color Changes

### Change to Green Theme
```bash
UI__PRIMARY_COLOR=#10b981
UI__SECONDARY_COLOR=#059669
UI__AGENT_COLORS__FINANCIAL_ADVISOR=#10b981
```

### Change to Purple Theme
```bash
UI__PRIMARY_COLOR=#8b5cf6
UI__SECONDARY_COLOR=#7c3aed
UI__AGENT_COLORS__FINANCIAL_ADVISOR=#8b5cf6
```

## 📁 Project Navigation

```
backend/
├── 🔧 config/app_config.py          # ← MAIN CONFIG FILE (CHANGE EVERYTHING HERE)
├── 📄 .env                          # ← ENVIRONMENT VARIABLES
├── 📄 main.py                       # ← API SERVER
├── 📄 simple_agents.py              # ← AGENT LOGIC
├── 📁 core/services/llm_service.py  # ← LLM SERVICE
└── 📁 docs/CONFIGURATION.md         # ← DETAILED CONFIG GUIDE
```

## 🔍 Where to Look For...

| Want to Change | Look Here |
|----------------|-----------|
| **Ollama Model** | `.env` file → `OLLAMA__MODEL_NAME` |
| **UI Colors** | `.env` file → `UI__PRIMARY_COLOR` |
| **Database Settings** | `.env` file → `DATABASE__*` |
| **Agent Behavior** | `simple_agents.py` |
| **API Endpoints** | `main.py` |
| **Advanced Config** | `config/app_config.py` |

## ⚡ Super Quick Commands

```bash
# Check current config
python config/app_config.py

# Test LLM service
PYTHONPATH=/Users/vikasmaurya/Downloads/finance-wizardry-bot/backend python core/services/llm_service.py

# Restart with new config
pkill -f uvicorn && uvicorn main:app --reload --port 3000
```

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| **Model not found** | `ollama pull llama3.1:8b` |
| **Ollama not responding** | `ollama serve` |
| **Config not loading** | Check `.env` file exists |
| **Import errors** | `source ./venv/bin/activate` |

## 📚 Full Documentation

For detailed configuration options, see:
- `docs/CONFIGURATION.md` - Complete config guide
- `PROJECT_STRUCTURE.md` - Folder organization
- `config/app_config.py` - All available settings
