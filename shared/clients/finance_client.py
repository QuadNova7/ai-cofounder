"""In-Process Finance Domain Client Wrapper."""

from shared.contracts.idea import IdeaAnalysisOutput
from shared.contracts.market import MarketResearchOutput
from shared.contracts.business_model import BusinessModelOutput
from shared.contracts.revenue import RevenueEstimationOutput


class FinanceClient:
    """In-process client wrapper for Finance domain engine."""

    def __init__(self):
        pass

    def estimate_revenue(
        self,
        idea: IdeaAnalysisOutput,
        market: MarketResearchOutput,
        business_model: BusinessModelOutput,
        horizon_months: int = 12
    ) -> RevenueEstimationOutput:
        from services.finance.app.interface import run_revenue_estimation
        return run_revenue_estimation(
            idea=idea,
            market=market,
            business_model=business_model,
            horizon_months=horizon_months
        )
