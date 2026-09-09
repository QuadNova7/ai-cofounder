"""Marketing Output Domain Strict Interface.

Exposes public entrypoints for Marketing / GTM Plan Generation and
final Startup Roadmap compilation.
All interactions from orchestrator or other agents must pass through this interface.
"""

from typing import List, Dict, Optional
from shared.contracts.idea import IdeaAnalysisOutput, FounderInput
from shared.contracts.market import MarketResearchOutput
from shared.contracts.business_model import BusinessModelOutput
from shared.contracts.revenue import RevenueEstimationOutput
from shared.contracts.marketing import MarketingPlanOutput, Milestone
from shared.contracts.roadmap import StartupRoadmap
from shared.contracts.venture_state import VentureState

from app.agents.marketing.agent import MarketingAgent


def run_marketing_plan(
    idea: IdeaAnalysisOutput,
    market: MarketResearchOutput,
    business_model: BusinessModelOutput,
    revenue: RevenueEstimationOutput,
    founder: Optional[FounderInput] = None
) -> MarketingPlanOutput:
    """Generates the GTM strategy, channel mix, positioning, and 90-day (12-week) execution plan."""
    agent = MarketingAgent()
    return agent.generate_plan(
        idea=idea,
        market=market,
        business_model=business_model,
        revenue=revenue,
        founder=founder
    )


def run_roadmap_synthesis(state: VentureState) -> StartupRoadmap:
    """Synthesizes all completed domain outputs into the final unified StartupRoadmap."""
    if not (state.idea_analysis and state.market_research and state.business_model and state.revenue_estimation and state.marketing_plan):
        raise ValueError("Cannot synthesize StartupRoadmap: All upstream domain stages must be completed.")

    # Compute overall confidence score as weighted composite
    critic_score = state.market_validation.confidence_score if state.market_validation else 0.8
    market_score = state.market_research.confidence_score
    overall_confidence = round((critic_score * 0.5) + (market_score * 0.5), 2)

    idea_text = getattr(state.founder_input, "startup_idea", None) or getattr(state.founder_input, "idea_description", "New Venture")
    venture_name = idea_text[:30] if idea_text else "New Venture"

    return StartupRoadmap(
        venture_id=state.venture_id,
        venture_name=venture_name,
        founder_input=state.founder_input,
        idea_analysis=state.idea_analysis,
        market_research=state.market_research,
        business_model=state.business_model,
        revenue_estimation=state.revenue_estimation,
        marketing_plan=state.marketing_plan,
        overall_confidence_score=overall_confidence,
        executive_summary=(
            f"Venture Roadmap for '{idea_text[:40]}...': "
            f"Targeting {', '.join(state.idea_analysis.target_users or state.idea_analysis.target_customer_segments if hasattr(state.idea_analysis, 'target_customer_segments') else state.idea_analysis.target_users)} with estimated SOM of "
            f"${state.market_research.som_estimate:,.0f}. "
            f"Moderate 12-month projected ARR stands at ${state.revenue_estimation.scenarios[1].month_12_revenue * 12:,.0f}."
        )
    )
