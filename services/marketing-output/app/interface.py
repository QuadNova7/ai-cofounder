"""Marketing Output Domain Strict Interface.

Exposes public entrypoints for Marketing / GTM Plan Generation and
final Startup Roadmap compilation.
All interactions from orchestrator or other agents must pass through this interface.
"""

from typing import List, Dict
from shared.contracts.idea import IdeaAnalysisOutput, FounderInput
from shared.contracts.market import MarketResearchOutput
from shared.contracts.business_model import BusinessModelOutput
from shared.contracts.revenue import RevenueEstimationOutput
from shared.contracts.marketing import MarketingPlanOutput, Milestone
from shared.contracts.roadmap import StartupRoadmap
from shared.contracts.venture_state import VentureState


def run_marketing_plan(
    idea: IdeaAnalysisOutput,
    market: MarketResearchOutput,
    business_model: BusinessModelOutput,
    revenue: RevenueEstimationOutput
) -> MarketingPlanOutput:
    """Generates the GTM strategy, channel mix, positioning, and 90-day execution plan."""
    return MarketingPlanOutput(
        positioning_statement=f"For {', '.join(idea.target_customer_segments)}, our solution delivers {idea.refined_value_proposition}.",
        priority_channels=[
            "Content Marketing & Technical SEO",
            "Product Hunt & Founder Communities",
            "Direct B2B Outreach via LinkedIn"
        ],
        messaging_framework={
            "headline": idea.refined_value_proposition,
            "subheadline": "Automate early-stage startup workflows with grounded intelligence.",
            "proof_point": "Backed by deterministic financial forecasting and verified market benchmarks."
        },
        gtm_90_day_plan=[
            Milestone(
                month=1,
                focus="Private Beta & User Validation",
                target_kpi="10 active pilot teams",
                deliverables=["MVP Landing page", "Closed beta onboarding", "Feedback interviews"]
            ),
            Milestone(
                month=2,
                focus="Community Launch & Content Engine",
                target_kpi="100 signups, 15% conversion to active",
                deliverables=["Public launch on Product Hunt", "Technical blog articles", "Webinar demonstration"]
            ),
            Milestone(
                month=3,
                focus="Monetization & Paid Acquisition Testing",
                target_kpi="25 paying customers, CAC < $150",
                deliverables=["Self-serve billing rollout", "Initial search ad tests", "Case study publication"]
            )
        ],
        acquisition_tactics=[
            "High-intent organic search keywords",
            "Founder directory listings",
            "Interactive demo playground"
        ],
        budget_allocation={
            "content_and_seo": 0.40,
            "paid_experiments": 0.35,
            "events_and_community": 0.25
        },
        prioritized_next_actions=[
            "Deploy landing page with waitlist capture",
            "Conduct 10 structured customer discovery interviews",
            "Finalize MVP feature scope for beta launch"
        ]
    )


def run_roadmap_synthesis(state: VentureState) -> StartupRoadmap:
    """Synthesizes all completed domain outputs into the final unified StartupRoadmap."""
    if not (state.idea_analysis and state.market_research and state.business_model and state.revenue_estimation and state.marketing_plan):
        raise ValueError("Cannot synthesize StartupRoadmap: All upstream domain stages must be completed.")

    # Compute overall confidence score as weighted composite
    critic_score = state.market_validation.confidence_score if state.market_validation else 0.8
    market_score = state.market_research.confidence_score
    overall_confidence = round((critic_score * 0.5) + (market_score * 0.5), 2)

    return StartupRoadmap(
        venture_id=state.venture_id,
        venture_name=state.founder_input.idea_description[:30] if state.founder_input.idea_description else "New Venture",
        founder_input=state.founder_input,
        idea_analysis=state.idea_analysis,
        market_research=state.market_research,
        business_model=state.business_model,
        revenue_estimation=state.revenue_estimation,
        marketing_plan=state.marketing_plan,
        overall_confidence_score=overall_confidence,
        executive_summary=(
            f"Venture Roadmap for '{state.founder_input.idea_description[:40]}...': "
            f"Targeting {', '.join(state.idea_analysis.target_customer_segments)} with estimated SOM of "
            f"${state.market_research.som_estimate:,.0f}. "
            f"Moderate 12-month projected ARR stands at ${state.revenue_estimation.scenarios[1].month_12_revenue * 12:,.0f}."
        )
    )
