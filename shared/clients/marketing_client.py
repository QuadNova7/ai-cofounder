"""In-Process Marketing Domain Client Wrapper."""

from shared.contracts.idea import IdeaAnalysisOutput
from shared.contracts.market import MarketResearchOutput
from shared.contracts.business_model import BusinessModelOutput
from shared.contracts.revenue import RevenueEstimationOutput
from shared.contracts.marketing import MarketingPlanOutput
from shared.contracts.roadmap import StartupRoadmap
from shared.contracts.venture_state import VentureState


class MarketingClient:
    """In-process client wrapper for Marketing and Roadmap synthesis domain."""

    def __init__(self):
        pass

    def generate_marketing_plan(
        self,
        idea: IdeaAnalysisOutput,
        market: MarketResearchOutput,
        business_model: BusinessModelOutput,
        revenue: RevenueEstimationOutput
    ) -> MarketingPlanOutput:
        from services.marketing_output.app.interface import run_marketing_plan
        return run_marketing_plan(
            idea=idea,
            market=market,
            business_model=business_model,
            revenue=revenue
        )

    def compile_startup_roadmap(self, state: VentureState) -> StartupRoadmap:
        from services.marketing_output.app.interface import run_roadmap_synthesis
        return run_roadmap_synthesis(state=state)
