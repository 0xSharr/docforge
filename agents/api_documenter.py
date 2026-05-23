"""API Documenter Agent — generates function signatures, parameters, return values, and NatSpec."""

from agents.base import BaseAgent

SYSTEM_PROMPT = """You are the API Documenter agent for DocForge. Your job is to analyze Solidity smart contract code and produce comprehensive API documentation.

For EVERY public/external function, generate:
1. Function signature with full type info
2. @notice and @dev NatSpec comments
3. @param for each parameter with type and description
4. @return for each return value with type and description
5. Access modifier and mutability (view/pure/payable)
6. Events emitted by the function
7. Revert conditions

Format output as structured Markdown with clear headers per contract, then per function.
Include a summary table at the top listing all functions with one-line descriptions.
Also generate ready-to-use NatSpec documentation that can be pasted directly above each function."""

USER_PROMPT_TEMPLATE = """Analyze the following Solidity smart contract code and produce complete API documentation:

```solidity
{code}
```

Generate:
1. A function summary table
2. Detailed documentation for each function
3. Ready-to-use NatSpec comments for every function"""


class APIDocumenter(BaseAgent):
    name = "api_documenter"

    async def run(self, solidity_code: str) -> str:
        return await self.call_llm(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=USER_PROMPT_TEMPLATE.format(code=solidity_code)
        )
