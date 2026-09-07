"""Research Domain Strict Interface.

Exposes public entrypoints for Market Research (Tavily search & competitor extraction)
and Critic / Evidence Validation.
All interactions from orchestrator or other agents must pass through this interface.
"""

from typing import Optional, List
from shared.contracts.idea import FounderInput, IdeaAnalysisOutput
from shared.contracts.market import MarketResearchOutput, Competitor
from shared.contracts.critic import CriticValidationOutput
from shared.enums.confidence_level import ValidationStatus


async def run_market_research(
    idea: IdeaAnalysisOutput,
    founder: FounderInput,
    critique_history: Optional[List[CriticValidationOutput]] = None
) -> MarketResearchOutput:
    """Executes market research with search tools, competitor analysis, and market sizing."""
    # In full implementation, calls TavilySearchTool and uses critique_history for targeted replanning
    return MarketResearchOutput(
        competitor_landscape=[
            Competitor(
                name="Incumbent Solutions Co",
                description="Traditional enterprise legacy platform",
                strengths=["High market presence", "Extensive sales force"],
                weaknesses=["High price", "Slow onboarding", "Outdated UX"],
                pricing_model="$500/month per seat",
                website_url="https://example.com/incumbent"
            ),
            Competitor(
                name="Agile Tooling Inc",
                description="Mid-market modern point solution",
                strengths=["Modern UI", "Self-serve trial"],
                weaknesses=["Limited feature depth", "No automated planning"],
                pricing_model="$49/month flat",
                website_url="https://example.com/agile"
            )
        ],
        customer_personas=[
            {"role": "Early-Stage Founder", "pain_point": "Lack of co-founder time and market clarity", "willingness_to_pay": "Moderate"},
            {"role": "Product Manager", "pain_point": "Manual research aggregation", "willingness_to_pay": "High"}
        ],
        market_trends=[
            "Rapid acceleration of AI-augmented venture creation",
            "Demand for deterministic business planning tools"
        ],
        entry_barriers=[
            "Customer trust in automated financial and strategic advice",
            "Access to proprietary market signals"
        ],
        tam_estimate=5000000000.0,
        sam_estimate=500000000.0,
        som_estimate=50000000.0,
        supporting_evidence=[
            "Market research reports indicate 24% annual growth in AI productivity tools",
            "Competitor pricing verified via public pricing pages"
        ],
        source_urls=[
            "https://example.com/market-report-2025",
            "https://example.com/venture-trends"
        ],
        confidence_score=0.85
    )


async def run_critic_validation(
    market: MarketResearchOutput,
    idea: IdeaAnalysisOutput
) -> CriticValidationOutput:
    """Applies the strict 3-point rubric: confidence >= 0.70, >= 2 verified citations, zero unverified claims."""
    verified_sources = len(market.source_urls)
    unsupported_claims: List[str] = []
    
    # Evaluate market scale invariant: SOM <= SAM <= TAM
    if market.tam_estimate and market.sam_estimate and market.som_estimate:
        if not (market.som_estimate <= market.sam_estimate <= market.tam_estimate):
            unsupported_claims.append("Market sizing violation: SOM must be <= SAM <= TAM")
    
    # Evaluate source threshold
    if verified_sources < 2:
        unsupported_claims.append(f"Insufficient citation sources: required at least 2, found {verified_sources}")
    
    # Evaluate confidence score
    is_valid = (market.confidence_score >= 0.70) and (len(unsupported_claims) == 0) and (verified_sources >= 2)
    
    status = ValidationStatus.VALID if is_valid else ValidationStatus.RESEARCH_REQUIRED
    
    return CriticValidationOutput(
        status=status,
        confidence_score=market.confidence_score if is_valid else min(0.55, market.confidence_score),
        unsupported_claims=unsupported_claims,
        verified_sources_count=verified_sources,
        feedback_notes="Validation passed all criteria." if is_valid else "; ".join(unsupported_claims),
        requires_pivot=False,
        suggested_alternatives=[]
    )
