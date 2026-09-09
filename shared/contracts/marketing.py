from typing import List, Dict, Optional
from pydantic import Field
from shared.contracts.base import BaseContract

class Milestone(BaseContract):
    month: int
    week: Optional[int] = None
    focus: str
    target_kpi: str
    deliverables: List[str]

class MarketingPlanOutput(BaseContract):
    positioning_statement: str
    priority_channels: List[str]
    messaging_framework: Dict[str, str]
    gtm_90_day_plan: List[Milestone]
    acquisition_tactics: List[str]
    budget_allocation: Dict[str, float]
    prioritized_next_actions: List[str]
    venture_archetype: Optional[str] = None
    target_cac: Optional[float] = None
    estimated_ltv: Optional[float] = None
    cac_payback_months: Optional[float] = None
    budget_breakdown_dollars: Optional[Dict[str, float]] = None
    warnings: List[str] = Field(default_factory=list)

