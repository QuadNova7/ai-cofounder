"""Orchestrator REST API Routes.

Implements venture pipeline management, state hydration, and
Human-in-the-Loop (HITL) review actions.
"""

from typing import Optional, Literal, Dict, Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from shared.contracts.idea import FounderInput
from shared.contracts.venture_state import VentureState
from shared.enums.workflow_status import WorkflowStage
from shared.utils.ids import generate_venture_id

router = APIRouter()

# In-memory store for active venture states in development / demo
_active_ventures: Dict[str, VentureState] = {}


class HumanReviewPayload(BaseModel):
    action: Literal["PROCEED_ANYWAY", "OVERRIDE_ASSUMPTIONS", "ABORT"]
    notes: Optional[str] = Field(default=None, description="Optional founder rationale or parameter override notes")


@router.post("/ventures/start", status_code=status.HTTP_201_CREATED)
async def start_venture(input_data: FounderInput):
    """Initializes a new venture state and kicks off the multi-agent pipeline."""
    venture_id = generate_venture_id()
    initial_state = VentureState(
        venture_id=venture_id,
        founder_input=input_data,
        current_stage=WorkflowStage.INITIALIZED
    )
    _active_ventures[venture_id] = initial_state
    return {
        "venture_id": venture_id,
        "status": initial_state.current_stage,
        "message": "Venture workflow initialized successfully."
    }


@router.get("/ventures/{venture_id}")
async def get_venture_state(venture_id: str):
    """State Hydration Endpoint: Returns the latest durable VentureState snapshot."""
    if venture_id not in _active_ventures:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venture with ID '{venture_id}' not found."
        )
    return _active_ventures[venture_id]


@router.post("/ventures/{venture_id}/review")
async def submit_human_review(venture_id: str, review: HumanReviewPayload):
    """Human-in-the-Loop (HITL) Resume API.
    
    Allows founder to unpause the pipeline when human review is required.
    Actions:
    - PROCEED_ANYWAY: Accept warnings and advance to next stage.
    - OVERRIDE_ASSUMPTIONS: Incorporate founder notes and re-run active stage.
    - ABORT: Terminate pipeline as FAILED.
    """
    if venture_id not in _active_ventures:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venture with ID '{venture_id}' not found."
        )

    state = _active_ventures[venture_id]
    state.human_review_required = False
    state.human_review_notes = review.notes

    if review.action == "ABORT":
        state.current_stage = WorkflowStage.FAILED
        state.warnings.append(f"Venture aborted by founder: {review.notes or 'No reason provided.'}")
        return {"venture_id": venture_id, "status": state.current_stage, "action_taken": "ABORTED"}

    if review.action == "PROCEED_ANYWAY":
        state.warnings.append(f"Founder override accepted: {review.notes or 'Proceeded past review threshold.'}")
        return {"venture_id": venture_id, "status": "RESUMED", "action_taken": "PROCEEDED"}

    if review.action == "OVERRIDE_ASSUMPTIONS":
        state.warnings.append(f"Assumptions overridden by founder: {review.notes}")
        return {"venture_id": venture_id, "status": "RESUMED", "action_taken": "ASSUMPTIONS_OVERRIDDEN"}

    return {"venture_id": venture_id, "status": "RESUMED"}
