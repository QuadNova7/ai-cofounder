"""In-Process Research Domain Client Wrapper."""

from typing import Optional, List
from shared.contracts.idea import FounderInput, IdeaAnalysisOutput
from shared.contracts.market import MarketResearchOutput
from shared.contracts.critic import CriticValidationOutput


class ResearchClient:
    """In-process client wrapper for Research domain and Critic validation."""

    def __init__(self):
        pass

    async def conduct_market_research(
        self,
        idea: IdeaAnalysisOutput,
        founder: FounderInput,
        critique_history: Optional[List[CriticValidationOutput]] = None
    ) -> MarketResearchOutput:
        from services.research.app.interface import run_market_research
        return await run_market_research(idea=idea, founder=founder, critique_history=critique_history)

    async def validate_market_evidence(
        self,
        market: MarketResearchOutput,
        idea: IdeaAnalysisOutput
    ) -> CriticValidationOutput:
        from services.research.app.interface import run_critic_validation
        return await run_critic_validation(market=market, idea=idea)
