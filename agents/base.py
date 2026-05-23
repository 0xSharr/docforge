"""Base agent class with shared LLM caller, retry logic, and token tracking."""

import asyncio
import logging
import os
import time
from typing import Optional

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)


class TokenTracker:
    """Persistent token usage tracker backed by SQLite."""

    def __init__(self, db_path: str = "data/tokens.db"):
        self.db_path = db_path
        self._ensure_dir()
        self._conn = None

    def _ensure_dir(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    async def init(self):
        import aiosqlite
        self._conn = await aiosqlite.connect(self.db_path)
        await self._conn.execute("""
            CREATE TABLE IF NOT EXISTS token_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent TEXT NOT NULL,
                model TEXT NOT NULL,
                prompt_tokens INTEGER NOT NULL,
                completion_tokens INTEGER NOT NULL,
                total_tokens INTEGER NOT NULL,
                latency_ms REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await self._conn.commit()

    async def record(self, agent: str, model: str, prompt_tokens: int,
                     completion_tokens: int, latency_ms: float):
        total = prompt_tokens + completion_tokens
        await self._conn.execute(
            "INSERT INTO token_usage (agent, model, prompt_tokens, completion_tokens, total_tokens, latency_ms) VALUES (?, ?, ?, ?, ?, ?)",
            (agent, model, prompt_tokens, completion_tokens, total, latency_ms)
        )
        await self._conn.commit()

    async def get_stats(self) -> dict:
        cursor = await self._conn.execute(
            "SELECT agent, COUNT(*), SUM(prompt_tokens), SUM(completion_tokens), SUM(total_tokens), AVG(latency_ms) FROM token_usage GROUP BY agent"
        )
        rows = await cursor.fetchall()
        stats = {}
        total_all = 0
        for row in rows:
            agent, calls, prompt, completion, total, avg_latency = row
            stats[agent] = {
                "calls": calls,
                "prompt_tokens": prompt,
                "completion_tokens": completion,
                "total_tokens": total,
                "avg_latency_ms": round(avg_latency, 2)
            }
            total_all += total
        cursor2 = await self._conn.execute("SELECT COUNT(*), SUM(total_tokens) FROM token_usage")
        row2 = await cursor2.fetchone()
        return {
            "by_agent": stats,
            "total_calls": row2[0],
            "total_tokens": row2[1] or 0
        }

    async def close(self):
        if self._conn:
            await self._conn.close()


class BaseAgent:
    """Base class for all DocForge agents with retry + token tracking."""

    name: str = "base"

    def __init__(self, client: AsyncOpenAI, model: str, tracker: TokenTracker):
        self.client = client
        self.model = model
        self.tracker = tracker

    async def call_llm(self, system_prompt: str, user_prompt: str,
                       max_retries: int = 3) -> str:
        for attempt in range(max_retries):
            try:
                start = time.monotonic()
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.3,
                )
                latency_ms = (time.monotonic() - start) * 1000
                usage = response.usage
                await self.tracker.record(
                    agent=self.name,
                    model=self.model,
                    prompt_tokens=usage.prompt_tokens,
                    completion_tokens=usage.completion_tokens,
                    latency_ms=latency_ms,
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.warning(f"[{self.name}] LLM call attempt {attempt+1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)

    async def run(self, solidity_code: str) -> str:
        raise NotImplementedError
