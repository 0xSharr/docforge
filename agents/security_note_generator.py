"""Security Note Generator Agent — security considerations per function, known vulnerability patterns."""

from agents.base import BaseAgent

SYSTEM_PROMPT = """You are the Security Note Generator agent for DocForge. Analyze Solidity smart contract code and produce security documentation.

For each function, generate:
1. Security risk level (Low / Medium / High / Critical)
2. Reentrancy risk assessment
3. Access control analysis (who can call this?)
4. Input validation checks
5. Known vulnerability patterns detected (e.g., reentrancy, integer overflow, front-running, oracle manipulation, flash loan attack surface)
6. Gas griefing vectors
7. Centralization risks
8. Recommendations for improvement

Also provide an overall security summary with:
- Risk score (1-10)
- Top 3 critical findings
- Audit checklist (items to verify before deployment)"""

USER_PROMPT_TEMPLATE = """Analyze the security characteristics of this Solidity code:

```solidity
{code}
```

Generate per-function security notes and an overall security assessment with risk score and audit checklist."""


class SecurityNoteGenerator(BaseAgent):
    name = "security_note_generator"

    async def run(self, solidity_code: str) -> str:
        return await self.call_llm(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=USER_PROMPT_TEMPLATE.format(code=solidity_code)
        )
