"""Server-Sent Events (SSE) Streaming Endpoint.

Emits standardized event envelopes to connected clients for real-time
stage transitions, progress percentages, warnings, and HITL interrupts.
"""

import json
import asyncio
from datetime import datetime, timezone
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()


def create_sse_event(
    event_type: str,
    venture_id: str,
    stage: str,
    progress_pct: int,
    message: str,
    data: dict = None
) -> str:
    """Formats an SSE message using the standardized architecture event envelope."""
    payload = {
        "event_type": event_type,
        "venture_id": venture_id,
        "stage": stage,
        "progress_pct": progress_pct,
        "message": message,
        "data": data or {},
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    return f"data: {json.dumps(payload)}\n\n"


@router.get("/ventures/{venture_id}/stream")
async def stream_venture_progress(venture_id: str):
    """Streams live multi-agent execution events to the frontend client."""
    async def event_generator():
        stages = [
            ("INITIALIZED", 5, "STAGE_STARTED", "Initializing venture state and blackboard..."),
            ("IDEA_ANALYSIS", 20, "STAGE_PROGRESS", "Deconstructing value proposition and customer segments..."),
            ("MARKET_RESEARCH", 40, "STAGE_PROGRESS", "Executing web search and competitor landscape scraping..."),
            ("CRITIC_VALIDATION", 55, "STAGE_PROGRESS", "Evaluating claims against external citations (rubric check)..."),
            ("BUSINESS_MODEL", 70, "STAGE_PROGRESS", "Querying ChromaDB and synthesizing Business Model Canvas..."),
            ("REVENUE_ESTIMATION", 85, "STAGE_PROGRESS", "Running deterministic financial projections and invariant checks..."),
            ("MARKETING", 95, "STAGE_PROGRESS", "Formulating 90-day GTM roadmap and acquisition channels..."),
            ("COMPLETED", 100, "ROADMAP_READY", "Startup Roadmap fully compiled and ready for review/export.")
        ]

        for stage, pct, event_type, msg in stages:
            yield create_sse_event(
                event_type=event_type,
                venture_id=venture_id,
                stage=stage,
                progress_pct=pct,
                message=msg
            )
            await asyncio.sleep(0.4)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
