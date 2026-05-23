"""Architecture Analyzer Agent — contract relationships, inheritance, interaction diagrams."""

from agents.base import BaseAgent

SYSTEM_PROMPT = """You are the Architecture Analyzer agent for DocForge. Analyze Solidity smart contract code and produce architectural documentation.

Generate:
1. Contract inheritance hierarchy (with diagram in Mermaid syntax)
2. State variable catalog with types, visibility, and purpose
3. Interface implementations and abstract contracts
4. Contract interaction patterns (who calls whom, cross-contract calls)
5. Data flow diagram (Mermaid syntax)
6. Module dependency graph
7. Design patterns used (e.g., Proxy, Factory, Access Control)

Use Mermaid diagram syntax for all diagrams so they can render in Markdown."""

USER_PROMPT_TEMPLATE = """Analyze the architectural structure of this Solidity code:

```solidity
{code}
```

Provide:
1. Inheritance hierarchy (Mermaid diagram)
2. State variables catalog
3. Contract interactions
4. Data flow diagram (Mermaid)
5. Design patterns identified"""


class ArchitectureAnalyzer(BaseAgent):
    name = "architecture_analyzer"

    async def run(self, solidity_code: str) -> str:
        return await self.call_llm(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=USER_PROMPT_TEMPLATE.format(code=solidity_code)
        )
