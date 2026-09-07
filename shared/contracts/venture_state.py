from typing import List, Optional, Dict, Any
from pydantic import Field
from shared.contracts.base import TimestampedContract
from shared.contracts.idea import FounderInput, IdeaAnalysisOutput
from shared.contracts.market import MarketResearchOutput
from shared.contracts.critic import CriticValidationOutput
from shared.contracts.business_model import BusinessModelOutput
from shared.contracts.revenue import RevenueEstimationOutput
from shared.contracts.marketing import MarketingPlanOutput
from shared.contracts.roadmap import StartupRoadmap
from shared.enums.workflow_status import WorkflowStage

class VentureState(TimestampedContract):
    venture_id: str
    founder_input: FounderInput
    
    current_stage: WorkflowStage = WorkflowStage.INITIALIZED
    
    idea_analysis: Optional[IdeaAnalysisOutput] = None
    market_research: Optional[MarketResearchOutput] = None
    market_validation: Optional[CriticValidationOutput] = None
    business_model: Optional[BusinessModelOutput] = None
    revenue_estimation: Optional[RevenueEstimationOutput] = None
    marketing_plan: Optional[MarketingPlanOutput] = None
    
    final_roadmap: Optional[StartupRoadmap] = None
    
    critique_history: List[CriticValidationOutput] = Field(default_factory=list)
    retry_counts: Dict[str, int] = Field(default_factory=dict)
    market_replan_count: int = 0
    finance_retune_count: int = 0
    replan_count: int = 0
    warnings: List[str] = Field(default_factory=list)
    human_review_required: bool = False
    human_review_notes: Optional[str] = None
