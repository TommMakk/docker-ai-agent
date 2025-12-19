# Deploy AI Agent

Multi-agent AI system for intelligent email and research automation using LangGraph's supervisor pattern to orchestrate specialized agents.

## Overview

Three coordinated agents:
- **Email Agent**: Send and retrieve emails
- **Research Agent**: Conduct research and generate insights
- **Supervisor**: Route tasks between agents

Example: *"Research why it's good to go outside and email me the results"* - the system routes to Research Agent, which researches the topic and sends results via email.

## Quick Start

### Prerequisites
- Python 3.10+, Docker, PostgreSQL
- Gmail account with app password
- OpenAI API key (or local LLM via Ollama)

### Setup

1. Create `.env`:
```bash
OPENAI_API_KEY=your_key
OPENAI_MODEL_NAME=gpt-4o-mini
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/deploy_ai
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
API_KEY=your_secure_key
```

2. Start:
```bash
docker compose up
```

API available at: `http://localhost:8070/api/chats/`

## API

### POST /api/chats/
Send message through multi-agent system.

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"message": "Research AI and email me the results"}' \
  http://localhost:8070/api/chats/
```

### GET /api/chats/
Health check.

### GET /api/chats/recent/
List recent messages.

## Project Structure

```
backend/src/
├── main.py              # FastAPI app
└── api/
    ├── __init__.py      # API package initializer
    ├── db.py            # Database config
    ├── ai/              # Agent system
    │   ├── __init__.py  # AI package initializer
    │   ├── agents.py    # Multi-agent factory
    │   ├── llms.py      # LLM setup and adapters
    │   ├── tools.py     # Email tools (LangChain/LangGraph wrappers)
    │   ├── services.py  # AI services (structured-output helpers)
    │   ├── assistants.py# Experimental assistants and utilities
    │   └── schemas.py   # Pydantic/SQLModel schemas for AI outputs
    ├── chat/
    │   ├── __init__.py  # Chat package initializer
    │   ├── routing.py   # API endpoints for chat interactions
    │   ├── ai_services.py# Chat-specific AI helpers and runners
    │   └── models.py    # Request/DB models for chat messages
    └── myemailer/       # Email operations
        ├── __init__.py  # Myemailer package initializer
        ├── inbox_reader.py # IMAP inbox read wrapper
        ├── sender.py       # SMTP email sending
        └── gmail_imap_parser.py # Robust IMAP parsing utilities
```

## Environment Variables

| Variable | Required | Default |
|----------|----------|---------|
| OPENAI_API_KEY | Yes | - |
| DATABASE_URL | Yes | - |
| EMAIL_ADDRESS | Yes | - |
| EMAIL_PASSWORD | Yes | - |
| OPENAI_MODEL_NAME | No | gpt-4o-mini |
| OPENAI_BASE_URL | No | (for local LLM) |

## Gmail Setup

1. Enable 2-Step Verification
2. Generate App Password at [Google Account](https://myaccount.google.com/security)
3. Use generated password as EMAIL_PASSWORD

## Known Limitations

- Open source LLMs (Llama, Mistral) may struggle with tool calling due to weaker model capability
- Uses in-memory state; restarts lose conversation history
- Gmail-only email support
