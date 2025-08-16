# Configuration Guide

## 🔧 Easy Configuration Management

This guide shows you how to easily change settings like Ollama models, colors, and other configurations from a single location.

## 🚀 Quick Start - Change Ollama Model

### Method 1: Environment Variables (Recommended)

Create or edit `.env` file:

```bash
# Global Ollama model
OLLAMA__MODEL_NAME=llama3.1:8b

# Agent-specific models
OLLAMA__AGENT_MODELS__NEWS_INTELLIGENCE=deepseek-r1:1.5b
OLLAMA__AGENT_MODELS__FINANCIAL_ADVISOR=llama3.1:8b
OLLAMA__AGENT_MODELS__CREDIT_SPECIALIST=mistral:7b

# Ollama server settings
OLLAMA__BASE_URL=http://localhost:11434
OLLAMA__TEMPERATURE=0.7
OLLAMA__MAX_TOKENS=1000
```

### Method 2: Python Code

```python
from config.app_config import app_config

# Change global model
app_config.ollama.model_name = "llama3.1:8b"

# Change specific agent models
app_config.ollama.agent_models["financial_advisor"] = "codellama:13b"
app_config.ollama.agent_models["news_intelligence"] = "deepseek-r1:1.5b"
app_config.ollama.agent_models["credit_specialist"] = "mistral:7b"
```

### Method 3: Configuration File

```python
# Save current config to file
app_config.save_to_file("my_config.json")

# Load config from file
from config.app_config import AppConfig
app_config = AppConfig.load_from_file("my_config.json")
```

## 🎨 UI Color Customization

### Change Colors

```bash
# In .env file
UI__PRIMARY_COLOR=#10b981     # Green
UI__SECONDARY_COLOR=#3b82f6   # Blue
UI__ACCENT_COLOR=#f59e0b      # Amber

# Agent-specific colors
UI__AGENT_COLORS__NEWS_INTELLIGENCE=#3b82f6     # Blue
UI__AGENT_COLORS__FINANCIAL_ADVISOR=#10b981     # Green
UI__AGENT_COLORS__CREDIT_SPECIALIST=#8b5cf6     # Purple
```

### Or in Python:

```python
from config.app_config import app_config

# Change primary colors
app_config.ui.primary_color = "#10b981"      # Green
app_config.ui.secondary_color = "#3b82f6"    # Blue

# Change agent colors
app_config.ui.agent_colors["financial_advisor"] = "#8b5cf6"  # Purple
app_config.ui.agent_colors["news_intelligence"] = "#ef4444"   # Red
```

## 📰 News Configuration

### News Update Settings

```bash
# In .env file
NEWS__UPDATE_INTERVAL_MINUTES=30
NEWS__MAX_ARTICLES_PER_FETCH=50
NEWS__SENTIMENT_THRESHOLD=0.1
```

### Custom Financial Keywords

```python
from config.app_config import app_config

# Add custom keywords for news filtering
app_config.news.financial_keywords.extend([
    "cryptocurrency", "blockchain", "NFT", "DeFi",
    "mortgage rates", "housing market", "inflation data"
])
```

## 🗄️ Database Configuration

```bash
# In .env file
DATABASE__HOST=localhost
DATABASE__PORT=5432
DATABASE__NAME=finance_wizardry
DATABASE__USER=postgres
DATABASE__PASSWORD=mypassword
```

## 🔒 Security Settings

```bash
# In .env file
SECURITY__SECRET_KEY=your-super-secret-key
SECURITY__JWT_EXPIRY_HOURS=24
SECURITY__RATE_LIMIT_PER_MINUTE=60
```

## 📝 Logging Configuration

```bash
# In .env file
LOGGING__LEVEL=INFO
LOGGING__FILE_PATH=/var/log/finance-bot.log
```

## 🎯 Available Models

### Recommended Models by Use Case

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| `deepseek-r1:1.5b` | Small | Fast | Good | News analysis, quick responses |
| `llama3.1:8b` | Medium | Medium | Excellent | Financial advice, complex reasoning |
| `mistral:7b` | Medium | Medium | Very Good | Credit analysis, general tasks |
| `codellama:13b` | Large | Slow | Excellent | Code generation, technical analysis |
| `phi3:14b` | Large | Slow | Excellent | Research, detailed analysis |

### Performance Comparison

```python
# For speed-critical applications
app_config.ollama.agent_models = {
    "news_intelligence": "deepseek-r1:1.5b",    # Fastest
    "financial_advisor": "deepseek-r1:1.5b",    # Fastest
    "credit_specialist": "deepseek-r1:1.5b",    # Fastest
}

# For quality-critical applications
app_config.ollama.agent_models = {
    "news_intelligence": "llama3.1:8b",         # Best balance
    "financial_advisor": "codellama:13b",       # Best reasoning
    "credit_specialist": "mistral:7b",          # Good accuracy
}
```

## 🔧 Advanced Configuration

### Custom Agent Models

```python
# Create custom model mapping
custom_models = {
    "news_intelligence": "my-custom-news-model",
    "financial_advisor": "my-custom-finance-model",
    "credit_specialist": "my-custom-credit-model",
}

app_config.ollama.agent_models.update(custom_models)
```

### Runtime Model Switching

```python
from core.services.llm_service import get_llm_service

# Switch model for specific agent
llm_service = get_llm_service("financial_advisor")
llm_service.switch_model("llama3.1:8b", "financial_advisor")

# Or switch globally
from core.services.llm_service import switch_global_model
switch_global_model("mistral:7b")
```

## ✅ Configuration Validation

### Check Current Configuration

```python
from config.app_config import app_config

print("=== Current Configuration ===")
print(f"Environment: {app_config.environment}")
print(f"Database URL: {app_config.database.url}")
print(f"Ollama Model: {app_config.ollama.model_name}")
print(f"Primary Color: {app_config.ui.primary_color}")

print("\nAgent Models:")
for agent, model in app_config.ollama.agent_models.items():
    print(f"  {agent}: {model}")
```

### Health Checks

```python
from core.services.llm_service import LLMService

# Check if Ollama is available
llm_service = LLMService()
if llm_service.health_check():
    print("✅ Ollama service is available")
else:
    print("❌ Ollama service is not available")
```

## 🚨 Troubleshooting

### Common Issues

1. **Ollama not responding**
   ```bash
   # Check if Ollama is running
   curl http://localhost:11434/api/tags
   
   # Start Ollama if needed
   ollama serve
   ```

2. **Model not found**
   ```bash
   # Download required model
   ollama pull llama3.1:8b
   ```

3. **Configuration not loading**
   ```python
   # Force reload configuration
   from config.app_config import AppConfig
   app_config = AppConfig.load_from_env()
   ```

## 📚 Environment Variables Reference

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `OLLAMA__MODEL_NAME` | Default Ollama model | `deepseek-r1:1.5b` | `llama3.1:8b` |
| `OLLAMA__BASE_URL` | Ollama server URL | `http://localhost:11434` | `http://192.168.1.100:11434` |
| `OLLAMA__TEMPERATURE` | Response creativity | `0.7` | `0.5` |
| `OLLAMA__MAX_TOKENS` | Max response length | `1000` | `1500` |
| `DATABASE__HOST` | Database host | `localhost` | `192.168.1.50` |
| `UI__PRIMARY_COLOR` | Primary UI color | `#fbbf24` | `#10b981` |

This configuration system makes it incredibly easy to customize your Finance Wizardry Bot without touching the code!
