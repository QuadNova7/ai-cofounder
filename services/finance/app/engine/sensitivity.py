"""Price sensitivity with customer demand held constant across cases.

Customers still follow the original growth and churn assumptions. Price changes
do not cause customers to join or leave.
"""

import math
from collections.abc import Iterable

from .calculator import calculate_projections


def calculate_price_sensitivity(
    starting_customers: int,
    monthly_price: float,
    growth_rate: float,
    churn_rate: float,
    months: int = 12,
    *,
    monthly_fixed_cost: float,
    monthly_cost_per_customer: float,
    price_percentage_changes: Iterable[float] | None = None,
):
    """Return aggregate projection dictionaries for distinct price changes.

    Changes are decimal fractions (0.1 means +10%), defaulting to -0.1, 0,
    and 0.1. Preserve supplied order and append the baseline if omitted.
    Profit differences are signed monetary amounts, not percentage changes.
    Demand is held constant across cases; no price-driven acquisition or churn
    is modelled. All other input validation belongs to calculate_projections.
    """
    changes = []
    seen = set()
    supplied_changes = (
        (-0.1, 0.0, 0.1)
        if price_percentage_changes is None else price_percentage_changes
    )
    for change in supplied_changes:
        if (
            isinstance(change, bool)
            or not isinstance(change, (int, float))
            or not math.isfinite(change)
            or change < -1
        ):
            raise ValueError(
                "price_percentage_changes must contain finite numbers at least -1"
            )
        if change not in seen:
            changes.append(change)
            seen.add(change)
    if 0 not in seen:
        changes.append(0.0)

    projection_inputs = dict(
        starting_customers=starting_customers,
        growth_rate=growth_rate,
        churn_rate=churn_rate,
        months=months,
        monthly_fixed_cost=monthly_fixed_cost,
        monthly_cost_per_customer=monthly_cost_per_customer,
    )
    # Validate the original price before any arithmetic can mask invalid input.
    baseline = calculate_projections(monthly_price=monthly_price, **projection_inputs)
    baseline_profit = sum(month["modelled_profit"] for month in baseline)
    results = []
    for change in changes:
        adjusted_price = monthly_price if change == 0 else monthly_price * (1 + change)
        projections = baseline if change == 0 else calculate_projections(
            monthly_price=adjusted_price, **projection_inputs
        )
        total_profit = sum(month["modelled_profit"] for month in projections)
        results.append({
            "price_percentage_change": change,
            "adjusted_monthly_price": adjusted_price,
            "total_revenue": sum(month["revenue"] for month in projections),
            "total_costs": sum(month["total_cost"] for month in projections),
            "total_modelled_profit": total_profit,
            "profit_difference_from_baseline": total_profit - baseline_profit,
        })
    return results
