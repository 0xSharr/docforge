"""Changelog Generator Agent — diff-based changelog, breaking changes detection."""

from agents.base import BaseAgent

SYSTEM_PROMPT = """You are the Changelog Generator agent for DocForge. Given Solidity smart contract code, produce a structured changelog and version analysis.

Generate:
1. **Contract Version** — Detect pragma version, any version constants
2. **Change Detection** — Analyze the code and identify what looks like recent additions vs stable code
3. **Breaking Changes Template** — Document what changes would break existing integrations:
   - Function signature changes
   - Storage layout changes
   - Event changes
   - Modifier changes
   - State variable changes
4. **Migration Guide** — How to upgrade from previous versions (if upgradeable pattern detected)
5. **Changelog Entry** — A formatted changelog entry following Keep a Changelog format
6. **Deprecation Notices** — Flag any functions/contracts that appear deprecated or TODO

If only one version is provided, generate the current state as v1.0.0 documentation and provide a template for future changelog entries."""

USER_PROMPT_TEMPLATE = """Analyze this Solidity code and generate changelog documentation:

```solidity
{code}
```

Provide version info, breaking changes analysis, migration guide, and a formatted changelog entry."""


class ChangelogGenerator(BaseAgent):
    name = "changelog_generator"

    async def run(self, solidity_code: str) -> str:
        return await self.call_llm(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=USER_PROMPT_TEMPLATE.format(code=solidity_code)
        )
