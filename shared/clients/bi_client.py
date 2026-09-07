"""In-Process Business Intelligence Domain Client Wrapper."""

from shared.contracts.idea import FounderInput, IdeaAnalysisOutput
from shared.contracts.market import MarketResearchOutput
from shared.contracts.business_model import BusinessModelOutput


class BusinessIntelligenceClient:
    """In-process client wrapper for Business Intelligence and RAG BMC domain."""

    def __init__(self):
        pass

    async def analyze_idea(self, founder_input: FounderInput) -> IdeaAnalysisOutput:
        from services.business_intelligence.app.interface import run_idea_analysis
        return await run_idea_analysis(founder_input=founder_input)

    async def generate_business_model(
        self,
        idea: IdeaAnalysisOutput,
        market: MarketResearchOutput
    ) -> BusinessModelOutput:
        from services.business_intelligence.app.interface import run_business_model
        return await run_business_model(idea=idea, market=market)
