"""AI Co-Founder Monolithic Orchestrator Entrypoint."""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from services.orchestrator.app.api.routes import router as api_router
    from services.orchestrator.app.api.stream import router as stream_router
except ImportError:
    from app.api.routes import router as api_router
    from app.api.stream import router as stream_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler: Idempotent ChromaDB vector store seeding on startup."""
    persist_dir = os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma")
    try:
        try:
            from services.business_intelligence.app.rag.seed_vector_store import seed_chromadb_if_empty
        except ImportError:
            from app.rag.seed_vector_store import seed_chromadb_if_empty
        seed_chromadb_if_empty(persist_directory=persist_dir)
    except Exception as exc:
        print(f"[Startup Warning] Vector store seeding skipped: {exc}")
    yield


app = FastAPI(
    title="AI Co-Founder Orchestrator",
    description="Central LangGraph stateful multi-agent orchestration backend",
    version="0.1.0",
    lifespan=lifespan
)

# CORS configuration
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
app.include_router(stream_router, prefix="/api")


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "orchestrator", "topology": "monolith"}
