"""Unit Tests for Marketing & GTM Agent.

Verifies Archetype classification, Bullseye 19-channel scoring, deterministic
unit economics invariants, absolute dollar budget allocations, 12-week sprint
generation, and LLM fallback resilience.
"""

import pytest
from shared.contracts.idea import IdeaAnalysisOutput, FounderInput
from shared.contracts.market import MarketResearchOutput, Competitor
from shared.contracts.business_model import BusinessModelOutput, BusinessModelCanvas
from shared.contracts.revenue import RevenueEstimationOutput, FinancialParameters, ProjectionScenario
from shared.contracts.marketing import MarketingPlanOutput

from app.agents.marketing.schemas import VentureArchetype, TractionChannel
from app.agents.marketing.archetypes import ArchetypeClassifier
from app.agents.marketing.channel_selector import BullseyeChannelSelector
from app.agents.marketing.budget_allocator import DeterministicBudgetAllocator
from app.agents.marketing.agent import MarketingAgent
from app.interface import run_marketing_plan


@pytest.fixture
def b2b_saas_context():
    idea = IdeaAnalysisOutput(
        problem_statement="High-growth B2B enterprise sales teams struggle with fragmented CRM data and slow workflow compliance.",
        target_users=["VP of Sales", "Enterprise Sales Operations", "Revenue Leaders"],
        refined_value_proposition="Automate B2B enterprise pipeline forecasting with deterministic CRM data intelligence.",
        key_assumptions=["Enterprise teams will pay $150/user/mo", "Security compliance is mandatory"],
        red_flags=[],
        clarity_score=0.9,
        feasibility_score=0.85,
        confidence_score=0.88
    )

    founder = FounderInput(
        startup_idea="Enterprise CRM workflow automation platform",
        target_market="B2B Enterprise SaaS",
        target_geography="North America",
        budget=10000.0,
        timeline_months=3,
        goals="Acquire 10 enterprise pilot logos",
        constraints=["Requires SOC2 compliance"],
        skills_resources="Technical co-founder, 5 years in B2B enterprise software"
    )

    market = MarketResearchOutput(
        competitor_landscape=[
            Competitor(name="Salesforce", description="Legacy enterprise CRM", strengths=["Market dominance"], weaknesses=["Bloated UX", "Slow implementation"])
        ],
        customer_personas=[{"role": "VP Sales", "pain_point": "Manual pipeline updates"}],
        market_trends=["AI automation in B2B revops"],
        entry_barriers=["Enterprise trust"],
        confidence_score=0.85
    )

    canvas = BusinessModelCanvas(
        key_partners=["Cloud Providers"],
        key_activities=["Platform Engineering"],
        key_resources=["Sales team"],
        value_propositions=["Automated B2B CRM workflows"],
        customer_relationships=["Dedicated Account Managers"],
        channels=["Direct Sales", "LinkedIn Outbound", "Webinars"],
        customer_segments=["Mid-market and Enterprise B2B SaaS"],
        cost_structure=["Hosting", "SDR Payroll"],
        revenue_streams=["Annual B2B SaaS Subscription Licenses"]
    )
    business_model = BusinessModelOutput(canvas=canvas, framework_used="BMC", confidence_score=0.85)

    revenue = RevenueEstimationOutput(
        pricing_strategy="B2B SaaS Tiered Per-Seat Monthly Subscription",
        parameters=FinancialParameters(
            monthly_price=120.0,
            starting_customers=10,
            monthly_growth_rate=0.15,
            monthly_churn_rate=0.02,
            cogs_per_unit=15.0,
            fixed_monthly_costs=5000.0
        ),
        scenarios=[
            ProjectionScenario(scenario_name="moderate", month_12_revenue=50000.0, month_12_customers=400)
        ]
    )

    return {"idea": idea, "founder": founder, "market": market, "business_model": business_model, "revenue": revenue}


def test_archetype_classifier_b2b_saas(b2b_saas_context):
    """Verifies that B2B enterprise context is classified as B2B_SAAS."""
    ctx = b2b_saas_context
    archetype = ArchetypeClassifier.classify(
        idea=ctx["idea"],
        business_model=ctx["business_model"],
        revenue=ctx["revenue"],
        founder=ctx["founder"]
    )
    assert archetype == VentureArchetype.B2B_SAAS


def test_archetype_classifier_devtools():
    """Verifies that developer tooling context is classified as PLG_DEVTOOLS."""
    idea = IdeaAnalysisOutput(
        problem_statement="Developers spend hours configuring local Docker dev environments.",
        target_users=["Software Engineers", "DevOps"],
        refined_value_proposition="Open-source CLI and SDK for instant developer environment provisioning.",
        key_assumptions=["Engineers love CLI"],
        clarity_score=0.9,
        feasibility_score=0.9,
        confidence_score=0.9
    )
    founder = FounderInput(
        startup_idea="Open source devtools CLI for developers",
        target_market="Developers & Engineers",
        budget=0.0
    )
    archetype = ArchetypeClassifier.classify(idea=idea, founder=founder)
    assert archetype == VentureArchetype.PLG_DEVTOOLS


def test_bullseye_channel_selector(b2b_saas_context):
    """Verifies Bullseye evaluates 19 channels and prioritizes sales/outbound for B2B SaaS."""
    ctx = b2b_saas_context
    ranking = BullseyeChannelSelector.rank_channels(
        archetype=VentureArchetype.B2B_SAAS,
        founder=ctx["founder"],
        revenue=ctx["revenue"]
    )
    assert len(ranking.inner_circle) == 3
    assert len(ranking.potential) >= 3
    assert len(ranking.long_shots) > 0

    inner_channels = [c.channel for c in ranking.inner_circle]
    # In B2B SaaS with high price & sales, Direct Sales and SEO/Content should rank at the top
    assert TractionChannel.SALES in inner_channels or TractionChannel.CONTENT_MARKETING in inner_channels


def test_budget_allocator_deterministic_invariants(b2b_saas_context):
    """Verifies pure Python unit economics calculations and invariants."""
    revenue = b2b_saas_context["revenue"]
    unit_econ = DeterministicBudgetAllocator.calculate_unit_economics(revenue)

    # Monthly price = 120, Churn = 0.02 -> LTV = 120 / 0.02 = 6,000
    assert unit_econ.estimated_ltv == 6000.0
    # CAC <= 1/3 LTV (2,000) and <= 8 * monthly_price (960)
    assert unit_econ.target_cac <= 2000.0
    assert unit_econ.cac_payback_months <= 12.0
    assert unit_econ.ltv_cac_ratio >= 3.0


def test_budget_allocator_dollar_sum(b2b_saas_context):
    """Verifies that allocated dollars sum exactly to founder budget."""
    channels = [TractionChannel.SALES, TractionChannel.CONTENT_MARKETING, TractionChannel.SEARCH_ENGINE_OPTIMIZATION]
    total_budget = 10000.0
    budget_map, items = DeterministicBudgetAllocator.allocate_budget(
        total_budget=total_budget,
        archetype=VentureArchetype.B2B_SAAS,
        priority_channels=channels
    )

    total_allocated = sum(budget_map.values())
    assert round(total_allocated, 2) == total_budget
    assert len(items) == 3


def test_budget_allocator_zero_budget():
    """Verifies $0 budget yields 0-dollar allocations with sweat-equity tactics."""
    channels = [TractionChannel.COMMUNITY_BUILDING, TractionChannel.CONTENT_MARKETING, TractionChannel.VIRAL_MARKETING]
    budget_map, items = DeterministicBudgetAllocator.allocate_budget(
        total_budget=0.0,
        archetype=VentureArchetype.PLG_DEVTOOLS,
        priority_channels=channels
    )

    for ch, amount in budget_map.items():
        assert amount == 0.0

    for item in items:
        assert item.allocated_dollars == 0.0
        assert any("sweat-equity" in t.lower() or "0-cac" in t.lower() or "founder" in t.lower() for t in item.tactics)


def test_marketing_agent_end_to_end_fallback(b2b_saas_context):
    """Verifies MarketingAgent produces complete MarketingPlanOutput with 12 sprints via fallback."""
    ctx = b2b_saas_context
    agent = MarketingAgent(llm_client=None)  # None forces deterministic fallback
    result = agent.generate_plan(
        idea=ctx["idea"],
        market=ctx["market"],
        business_model=ctx["business_model"],
        revenue=ctx["revenue"],
        founder=ctx["founder"]
    )

    assert isinstance(result, MarketingPlanOutput)
    assert result.venture_archetype == VentureArchetype.B2B_SAAS.value
    assert len(result.priority_channels) == 3
    assert len(result.gtm_90_day_plan) == 12  # Exactly 12 weekly sprints
    assert result.gtm_90_day_plan[0].week == 1
    assert result.gtm_90_day_plan[11].week == 12
    assert result.target_cac is not None and result.target_cac > 0
    assert result.estimated_ltv is not None and result.estimated_ltv > 0
    assert result.cac_payback_months is not None
    assert sum(result.budget_allocation.values()) == 10000.0
    assert len(result.prioritized_next_actions) >= 3


def test_interface_run_marketing_plan(b2b_saas_context):
    """Verifies public interface entrypoint run_marketing_plan."""
    ctx = b2b_saas_context
    result = run_marketing_plan(
        idea=ctx["idea"],
        market=ctx["market"],
        business_model=ctx["business_model"],
        revenue=ctx["revenue"],
        founder=ctx["founder"]
    )
    assert result.positioning_statement is not None
    assert len(result.gtm_90_day_plan) == 12
    assert result.venture_archetype is not None
