"""DocForge — Multi-agent Smart Contract Documentation Generator.

Main FastAPI application with pipeline orchestration.
"""

import asyncio
import hashlib
import logging
import os
import time
import uuid
from contextlib import asynccontextmanager
from typing import Optional

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from openai import AsyncOpenAI

from agents.base import TokenTracker
from agents.api_documenter import APIDocumenter
from agents.architecture_analyzer import ArchitectureAnalyzer
from agents.security_note_generator import SecurityNoteGenerator
from agents.usage_example_generator import UsageExampleGenerator
from agents.changelog_generator import ChangelogGenerator
from agents.synthesis import SynthesisAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("docforge")

# In-memory document store
documents: dict = {}

# Token tracker instance
tracker = TokenTracker(db_path=os.getenv("TOKEN_DB_PATH", "data/tokens.db"))

# LLM config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await tracker.init()
    logger.info("DocForge started — token tracker initialized")
    yield
    await tracker.close()


app = FastAPI(
    title="DocForge",
    description="Multi-agent Smart Contract Documentation Generator — 5 specialized AI agents",
    version="1.0.0",
    lifespan=lifespan,
)


def get_client() -> AsyncOpenAI:
    return AsyncOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)


def get_agents(client: AsyncOpenAI) -> dict:
    return {
        "api_documenter": APIDocumenter(client, OPENAI_MODEL, tracker),
        "architecture_analyzer": ArchitectureAnalyzer(client, OPENAI_MODEL, tracker),
        "security_note_generator": SecurityNoteGenerator(client, OPENAI_MODEL, tracker),
        "usage_example_generator": UsageExampleGenerator(client, OPENAI_MODEL, tracker),
        "changelog_generator": ChangelogGenerator(client, OPENAI_MODEL, tracker),
    }


async def run_pipeline(doc_id: str, solidity_code: str):
    """Run the full multi-agent pipeline: fan-out to 5 agents, then synthesis."""
    client = get_client()
    agents = get_agents(client)
    synthesis = SynthesisAgent(client, OPENAI_MODEL, tracker)

    documents[doc_id]["status"] = "processing"
    documents[doc_id]["progress"] = "Running 5 specialized agents in parallel..."
    start_time = time.monotonic()

    try:
        # Fan-out: run all 5 agents in parallel
        tasks = {
            name: asyncio.create_task(agent.run(solidity_code))
            for name, agent in agents.items()
        }
        results = {}
        for name, task in tasks.items():
            results[name] = await task
            logger.info(f"[{doc_id}] Agent '{name}' completed")

        documents[doc_id]["progress"] = "Synthesizing unified documentation..."

        # Synthesis
        final_doc = await synthesis.run(results)
        elapsed = time.monotonic() - start_time

        documents[doc_id].update({
            "status": "completed",
            "progress": "Done",
            "result": final_doc,
            "agent_outputs": results,
            "elapsed_seconds": round(elapsed, 2),
        })
        logger.info(f"[{doc_id}] Pipeline completed in {elapsed:.2f}s")

    except Exception as e:
        logger.error(f"[{doc_id}] Pipeline failed: {e}")
        documents[doc_id].update({
            "status": "failed",
            "progress": f"Error: {str(e)}",
        })


@app.post("/document")
async def create_document(file: UploadFile = File(...)):
    """Upload a Solidity file and start the documentation pipeline."""
    content = await file.read()
    code = content.decode("utf-8", errors="replace")

    if len(code.strip()) == 0:
        raise HTTPException(status_code=400, detail="Empty file")

    doc_id = str(uuid.uuid4())[:12]
    code_hash = hashlib.sha256(code.encode()).hexdigest()[:16]

    documents[doc_id] = {
        "id": doc_id,
        "filename": file.filename,
        "code_hash": code_hash,
        "status": "queued",
        "progress": "Queued",
        "result": None,
        "agent_outputs": {},
        "elapsed_seconds": None,
    }

    # Start pipeline in background
    asyncio.create_task(run_pipeline(doc_id, code))

    return {"id": doc_id, "status": "queued", "filename": file.filename}


@app.get("/document/{doc_id}")
async def get_document(doc_id: str):
    """Get document status and result."""
    if doc_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    return documents[doc_id]


@app.get("/stats")
async def get_stats():
    """Get token usage statistics."""
    return await tracker.get_stats()


# Serve frontend
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.isdir(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


@app.get("/")
async def index():
    """Serve the frontend."""
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path) as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1>DocForge</h1><p>Frontend not found. Use the API at /docs</p>")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=True,
    )
