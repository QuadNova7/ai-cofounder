from typing import List, Dict, Any, Optional
from pydantic import Field
from shared.contracts.base import BaseContract

class FinancialParameters(BaseContract):
    monthly_price: float = Field(ge=0)
    starting_customers: int = Field(ge=0)
    monthly_growth_rate: float = Field(ge=0.0, le=1.0)
    monthly_churn_rate: float = Field(ge=0.0, le=1.0)
    cogs_per_unit: float = Field(default=0.0, ge=0)
    fixed_monthly_costs: float = Field(default=0.0, ge=0)

class ProjectionScenario(BaseContract):
    scenario_name: str  # "conservative", "moderate", "optimistic"
    month_12_revenue: float
    month_12_customers: int
    break_even_month: Optional[int] = None
    monthly_projections: List[Dict[str, Any]] = Field(default_factory=list)

class RevenueEstimationOutput(BaseContract):
    pricing_strategy: str
    parameters: FinancialParameters
    scenarios: List[ProjectionScenario]
    tam_sam_som_valid: bool = True
    assumptions_summary: List[str] = Field(default_factory=list)
