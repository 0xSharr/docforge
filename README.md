# DocForge — Multi-agent Smart Contract Documentation Generator

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![AI Agents](https://img.shields.io/badge/agents-5-brightgreen)
![MiMo Orbit](https://img.shields.io/badge/MiMo-Orbit-purple)

> **5 specialized AI agents that analyze your Solidity smart contracts and produce publication-ready documentation — API docs, architecture diagrams, security notes, usage examples, and changelogs.**

---

## ✨ Features

- **5 Specialized AI Agents** — each focused on a distinct documentation domain
- **Parallel Processing** — all agents run concurrently for maximum speed
- **Synthesis Agent** — merges all outputs into one unified, professional document
- **Token Tracking** — persistent SQLite tracking of all LLM API calls
- **Mermaid Diagrams** — auto-generated architecture and data flow diagrams
- **NatSpec Generation** — copy-pasteable NatSpec comments for your contracts
- **Security Analysis** — per-function risk assessment and audit checklist
- **Beautiful Web UI** — drag-and-drop upload with real-time progress
- **Docker Ready** — one command deployment

---

## 🏗️ Architecture

```
┌─────────────┐
│  Solidity   │  Upload .sol file
│  Source      │
└──────┬──────┘
       │
       ▼
┌──────────────┐     ┌─────────────────────┐
│   Chunk &    │────▶│  5 Agents (parallel) │
│   Dispatch   │     │                      │
└──────────────┘     │  1. API Documenter    │
                     │  2. Architecture      │
                     │  3. Security Notes    │
                     │  4. Usage Examples    │
                     │  5. Changelog         │
                     └──────────┬────────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │   Synthesis Agent    │
                     │   (merge & format)   │
                     └──────────┬────────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │  Unified Markdown    │
                     │  + NatSpec docs      │
                     └─────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key (or compatible endpoint)

### Installation

```bash
git clone https://github.com/0xSharr/docforge.git
cd docforge
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key
```

### Run

```bash
python app.py
# Open http://localhost:8000
```

### Docker

```bash
cp .env.example .env
# Edit .env with your API key
docker-compose up --build
# Open http://localhost:8000
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/document` | Upload Solidity file, start pipeline |
| `GET` | `/document/{id}` | Get document status and result |
| `GET` | `/stats` | Get token usage statistics |
| `GET` | `/` | Web frontend |
| `GET` | `/docs` | Swagger UI |

### Example: Upload a Contract

```bash
curl -X POST http://localhost:8000/document \
  -F "file=@MyContract.sol"
# Returns: {"id": "a1b2c3d4", "status": "queued", "filename": "MyContract.sol"}
```

### Example: Get Result

```bash
curl http://localhost:8000/document/a1b2c3d4
```

---

## 🤖 The 5 Agents

| Agent | Focus | Output |
|-------|-------|--------|
| **API Documenter** | Function signatures, params, returns | NatSpec + reference tables |
| **Architecture Analyzer** | Inheritance, interactions | Mermaid diagrams + catalog |
| **Security Note Generator** | Risk assessment, vulnerabilities | Per-function security notes |
| **Usage Example Generator** | Deployment, integration | Copy-pasteable code examples |
| **Changelog Generator** | Versioning, breaking changes | Migration guide + changelog |

---

## 💰 Token Consumption

DocForge tracks all LLM API calls in a persistent SQLite database.

Typical token usage for a medium-sized contract (~200 lines):
- **Per agent call**: ~2,000-4,000 tokens (prompt + completion)
- **Total pipeline**: ~15,000-25,000 tokens
- **Synthesis call**: ~5,000-8,000 tokens (merging all outputs)

Access live stats via `GET /stats`:
```json
{
  "total_calls": 12,
  "total_tokens": 45230,
  "by_agent": {
    "api_documenter": {"calls": 3, "total_tokens": 12400, "avg_latency_ms": 2340},
    "synthesis": {"calls": 3, "total_tokens": 18200, "avg_latency_ms": 4100}
  }
}
```

---

## 📁 Project Structure

```
docforge/
├── app.py                    # FastAPI application + pipeline orchestrator
├── agents/
│   ├── __init__.py
│   ├── base.py               # BaseAgent + TokenTracker (SQLite)
│   ├── api_documenter.py     # Function signatures & NatSpec
│   ├── architecture_analyzer.py  # Contract relationships & diagrams
│   ├── security_note_generator.py # Security analysis
│   ├── usage_example_generator.py # Code examples & integration
│   ├── changelog_generator.py # Versioning & breaking changes
│   └── synthesis.py          # Merges all outputs
├── frontend/
│   └── index.html            # Web UI
├── docs/
│   ├── ARCHITECTURE.md       # Detailed architecture doc
│   └── EXAMPLE_RUN.md        # Example pipeline run
├── proofs/                   # Example run outputs
├── .env.example
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── LICENSE
└── README.md
```

---

## 📄 License

MIT — see [LICENSE](LICENSE).

---

*Built for the MiMo Orbit grant program. Variant #11.*
