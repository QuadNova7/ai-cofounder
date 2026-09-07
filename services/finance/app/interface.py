"""Finance Domain Strict Interface.

Exposes public entrypoint for Revenue Estimation and deterministic scenario calculations.
All interactions from orchestrator or other agents must pass through this interface.
"""

from typing import Optional, List
from shared.contracts.idea import IdeaAnalysisOutput
from shared.contracts.market import MarketResearchOutput
from shared.contracts.business_model import BusinessModelOutput
from shared.contracts.revenue import (
    RevenueEstimationOutput,
    FinancialParameters,
    ProjectionScenario
)

try:
    from services.finance.app.engine.calculator import calculate_projections
    from services.finance.app.validation.invariants import verify_tam_sam_som
except ImportError:
    from app.engine.calculator import calculate_projections
    from app.validation.invariants import verify_tam_sam_som


def run_revenue_estimation(
    idea: IdeaAnalysisOutput,
    market: MarketResearchOutput,
    business_model: BusinessModelOutput,
    horizon_months: int = 12
) -> RevenueEstimationOutput:
    """Calculates deterministic 12-to-36 month revenue projections across 3 scenarios."""
    # Base parameters extracted or defaulted
    params = FinancialParameters(
        monthly_price=99.0,
        starting_customers=25,
        monthly_growth_rate=0.15,
        monthly_churn_rate=0.03,
        cogs_per_unit=15.0,
        fixed_monthly_costs=5000.0
    )

    # 1. Conservative: 70% growth, 130% churn
    cons_projections = calculate_projections(
        starting_customers=params.starting_customers,
        monthly_price=params.monthly_price,
        growth_rate=params.monthly_growth_rate * 0.7,
        churn_rate=min(0.99, params.monthly_churn_rate * 1.3),
        months=horizon_months
    )

    # 2. Moderate: Baseline parameters
    mod_projections = calculate_projections(
        starting_customers=params.starting_customers,
        monthly_price=params.monthly_price,
        growth_rate=params.monthly_growth_rate,
        churn_rate=params.monthly_churn_rate,
        months=horizon_months
    )

    # 3. Optimistic: 140% growth, 80% churn
    opt_projections = calculate_projections(
        starting_customers=params.starting_customers,
        monthly_price=params.monthly_price,
        growth_rate=params.monthly_growth_rate * 1.4,
        churn_rate=params.monthly_churn_rate * 0.8,
        months=horizon_months
    )

    # Validate market scale invariant
    tam = market.tam_estimate or 1000000000.0
    sam = market.sam_estimate or 100000000.0
    som = market.som_estimate or 10000000.0
    invariants_valid = verify_tam_sam_som(tam, sam, som)

    return RevenueEstimationOutput(
        pricing_strategy="Tiered B2B SaaS Monthly Subscription",
        parameters=params,
        scenarios=[
            ProjectionScenario(
                scenario_name="conservative",
                month_12_revenue=cons_projections[-1]["revenue"],
                month_12_customers=cons_projections[-1]["customers"],
                monthly_projections=cons_projections
            ),
            ProjectionScenario(
                scenario_name="moderate",
                month_12_revenue=mod_projections[-1]["revenue"],
                month_12_customers=mod_projections[-1]["customers"],
                monthly_projections=mod_projections
            ),
            ProjectionScenario(
                scenario_name="optimistic",
                month_12_revenue=opt_projections[-1]["revenue"],
                month_12_customers=opt_projections[-1]["customers"],
                monthly_projections=opt_projections
            )
        ],
        tam_sam_som_valid=invariants_valid,
        assumptions_summary=[
            f"Base monthly price: ${params.monthly_price}",
            f"Monthly growth rate assumption: {params.monthly_growth_rate * 100}%",
            f"Estimated monthly churn rate: {params.monthly_churn_rate * 100}%"
        ]
    )
