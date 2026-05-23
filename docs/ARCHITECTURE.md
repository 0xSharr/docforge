# DocForge Architecture

## Overview

DocForge uses a **fan-out / fan-in** pipeline pattern. When a Solidity file is uploaded, it is dispatched to 5 specialized AI agents running in parallel. Each agent produces domain-specific documentation. A synthesis agent then merges all outputs into a single, publication-ready document.

## Components

### 1. API Documenter (`agents/api_documenter.py`)
Analyzes every public/external function and generates:
- Function signature table
- Parameter documentation with types
- Return value documentation
- Ready-to-paste NatSpec comments (`@notice`, `@dev`, `@param`, `@return`)

### 2. Architecture Analyzer (`agents/architecture_analyzer.py`)
Maps the contract's structural relationships:
- Inheritance hierarchy (Mermaid diagrams)
- State variable catalog
- Interface implementations
- Cross-contract call patterns
- Design pattern identification

### 3. Security Note Generator (`agents/security_note_generator.py`)
Per-function security assessment:
- Reentrancy risk
- Access control analysis
- Input validation checks
- Known vulnerability pattern detection
- Overall risk score (1-10)
- Audit checklist

### 4. Usage Example Generator (`agents/usage_example_generator.py`)
Practical, copy-pasteable examples:
- Hardhat/Foundry deployment scripts
- ethers.js function call examples
- React integration snippets
- Foundry test skeletons
- Event listening patterns

### 5. Changelog Generator (`agents/changelog_generator.py`)
Version management documentation:
- Pragma and version detection
- Breaking changes analysis
- Migration guide template
- Keep a Changelog formatted entry

### 6. Synthesis Agent (`agents/synthesis.py`)
Takes all 5 agent outputs and produces one unified Markdown document with:
- Overview
- Architecture (with Mermaid diagrams)
- API Reference
- Security Considerations
- Usage Guide
- Changelog
- NatSpec Reference (ready to paste)

## Data Flow

```
Upload .sol → FastAPI endpoint → UUID assigned → Background task created
                                                    ↓
                                    Fan-out to 5 agents (asyncio.gather)
                                        ↓           ↓           ↓
                                    Agent 1     Agent 2 ...   Agent 5
                                        ↓           ↓           ↓
                                    Merge all outputs
                                        ↓
                                    Synthesis Agent
                                        ↓
                                    Unified Markdown + NatSpec
                                        ↓
                                    Stored in memory, returned via API
```

## Token Tracking

All LLM calls are recorded in SQLite (`data/tokens.db`):
- Agent name
- Model used
- Prompt tokens
- Completion tokens
- Latency (ms)
- Timestamp

Stats accessible via `GET /stats`.

## Tech Stack

- **Backend**: Python 3.12, FastAPI, AsyncOpenAI
- **Database**: SQLite (via aiosqlite) for token tracking
- **Frontend**: Vanilla HTML/CSS/JS (no build step)
- **Containerization**: Docker + docker-compose
