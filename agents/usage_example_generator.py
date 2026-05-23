"""Usage Example Generator Agent — code examples, deployment scripts, integration guides."""

from agents.base import BaseAgent

SYSTEM_PROMPT = """You are the Usage Example Generator agent for DocForge. Analyze Solidity smart contract code and produce practical usage documentation.

Generate:
1. **Deployment Scripts** — Hardhat (JavaScript/TypeScript) and Foundry deployment examples
2. **Function Call Examples** — JavaScript/TypeScript (ethers.js) examples for every public function
3. **Integration Guide** — How to integrate this contract with a frontend (React snippet)
4. **Testing Examples** — Foundry/Forge test file skeleton with key test cases
5. **Error Handling** — Common error codes/reverts and how to handle them in code
6. **Event Listening** — How to listen for and handle contract events

All code examples should be complete, copy-pasteable, and use modern best practices."""

USER_PROMPT_TEMPLATE = """Generate comprehensive usage examples for this Solidity contract:

```solidity
{code}
```

Provide deployment scripts, function call examples, integration guide, testing skeleton, and event handling examples."""


class UsageExampleGenerator(BaseAgent):
    name = "usage_example_generator"

    async def run(self, solidity_code: str) -> str:
        return await self.call_llm(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=USER_PROMPT_TEMPLATE.format(code=solidity_code)
        )
