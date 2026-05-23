"""Synthesis Agent — merges all agent outputs into unified documentation (Markdown + NatSpec)."""

from agents.base import BaseAgent

SYSTEM_PROMPT = """You are the Synthesis agent for DocForge. Your job is to merge outputs from 5 specialized agents into one unified, professional smart contract documentation.

You will receive outputs from:
1. **API Documenter** — Function signatures, params, NatSpec
2. **Architecture Analyzer** — Inheritance, interactions, diagrams
3. **Security Note Generator** — Risk assessments, audit checklist
4. **Usage Example Generator** — Code examples, deployment, integration
5. **Changelog Generator** — Version info, breaking changes, migration

Produce a single, well-structured Markdown document with these sections:
1. **Overview** — Brief summary of what the contract does
2. **Architecture** — Inheritance, design patterns, Mermaid diagrams
3. **API Reference** — Full function documentation with NatSpec
4. **Security Considerations** — Risk summary, per-function notes, audit checklist
5. **Usage Guide** — Deployment, integration, examples
6. **Changelog** — Version info, migration guide
7. **NatSpec Reference** — All NatSpec comments ready to paste

Ensure no duplication, consistent formatting, and professional quality.
Use proper Markdown headers, tables, code blocks, and Mermaid diagrams.
The document should be self-contained and publication-ready."""

USER_PROMPT_TEMPLATE = """Merge the following agent outputs into unified documentation:

## API Documenter Output:
{api_docs}

## Architecture Analyzer Output:
{architecture}

## Security Note Generator Output:
{security}

## Usage Example Generator Output:
{usage}

## Changelog Generator Output:
{changelog}

Produce a single, complete, publication-ready Markdown document."""


class SynthesisAgent(BaseAgent):
    name = "synthesis"

    async def run(self, agent_outputs: dict) -> str:
        return await self.call_llm(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=USER_PROMPT_TEMPLATE.format(
                api_docs=agent_outputs.get("api_documenter", ""),
                architecture=agent_outputs.get("architecture_analyzer", ""),
                security=agent_outputs.get("security_note_generator", ""),
                usage=agent_outputs.get("usage_example_generator", ""),
                changelog=agent_outputs.get("changelog_generator", ""),
            )
        )
