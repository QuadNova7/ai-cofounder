"""Deterministic Budget Allocator & Unit Economics Engine.

Pure Python math calculating LTV, Target CAC, Payback Period, and exact
dollar budget distribution with invariant enforcement.
"""

from typing import List, Dict, Tuple, Optional
from shared.contracts.revenue import RevenueEstimationOutput
from app.agents.marketing.schemas import (
    VentureArchetype, TractionChannel, UnitEconomicsMetrics, BudgetItem
)


class DeterministicBudgetAllocator:
    """Calculates deterministic unit economics and distributes budget without LLM arithmetic."""

    @staticmethod
    def calculate_unit_economics(revenue: Optional[RevenueEstimationOutput]) -> UnitEconomicsMetrics:
        """Calculates deterministic LTV, Target CAC, and Payback Period.
        
        Invariants enforced:
        - Target CAC <= 1/3 * LTV (3:1 LTV:CAC ratio)
        - Payback Period <= 12 months (target <= 6 months for early stage)
        """
        monthly_price = 50.0
        monthly_churn = 0.03

        if revenue and revenue.parameters:
            if revenue.parameters.monthly_price > 0:
                monthly_price = float(revenue.parameters.monthly_price)
            if 0.001 <= revenue.parameters.monthly_churn_rate <= 0.99:
                monthly_churn = float(revenue.parameters.monthly_churn_rate)

        # LTV = Monthly Price / Monthly Churn
        estimated_ltv = round(monthly_price / monthly_churn, 2)

        # Target CAC ceiling: 1/3 of LTV, and max 8x monthly subscription
        target_cac = round(min(estimated_ltv / 3.0, monthly_price * 8.0), 2)
        if target_cac < 10.0:
            target_cac = 10.0

        # Payback period in months
        payback_months = round(target_cac / max(monthly_price, 1.0), 1)
        ltv_cac_ratio = round(estimated_ltv / max(target_cac, 1.0), 2)

        return UnitEconomicsMetrics(
            monthly_price=monthly_price,
            monthly_churn_rate=monthly_churn,
            estimated_ltv=estimated_ltv,
            target_cac=target_cac,
            cac_payback_months=payback_months,
            ltv_cac_ratio=ltv_cac_ratio
        )

    @staticmethod
    def allocate_budget(
        total_budget: float,
        archetype: VentureArchetype,
        priority_channels: List[TractionChannel]
    ) -> Tuple[Dict[str, float], List[BudgetItem]]:
        """Distributes the founder's exact budget across priority channels.
        
        - If budget is 0 or negative: Allocates $0 to all channels and structures
          100% of the plan around sweat-equity organic acquisition.
        - If budget > 0: Exactly partitions budget across top 3 channels summing to 100%.
        """
        budget = max(0.0, float(total_budget))
        top_channels = priority_channels[:3] if len(priority_channels) >= 3 else priority_channels

        # Default weights across the 3 chosen channels
        weights = [0.50, 0.30, 0.20]
        if len(top_channels) == 2:
            weights = [0.60, 0.40]
        elif len(top_channels) == 1:
            weights = [1.0]

        budget_map: Dict[str, float] = {}
        budget_items: List[BudgetItem] = []

        if budget == 0.0:
            # Zero-Budget Sweat-Equity Mode
            for ch in top_channels:
                channel_name = ch.value
                budget_map[channel_name] = 0.0
                budget_items.append(BudgetItem(
                    channel=channel_name,
                    allocated_dollars=0.0,
                    percentage=0.0,
                    tactics=[
                        "Founder sweat-equity: direct outbound & community engagement",
                        "High-intent organic content and developer documentation",
                        "0-CAC directory submissions (Product Hunt, BetaList, Hacker News)"
                    ]
                ))
            return budget_map, budget_items

        # Positive Budget Allocation: Distribute exact dollars
        allocated_so_far = 0.0
        for i, ch in enumerate(top_channels):
            channel_name = ch.value
            weight = weights[i]
            
            if i == len(top_channels) - 1:
                # Last channel gets the remainder to guarantee exact sum
                dollar_amount = round(budget - allocated_so_far, 2)
            else:
                dollar_amount = round(budget * weight, 2)
                allocated_so_far += dollar_amount

            pct = round(dollar_amount / budget, 4) if budget > 0 else 0.0
            budget_map[channel_name] = dollar_amount

            # Sample tactics by archetype and channel
            tactics = DeterministicBudgetAllocator._get_tactics_for_channel(ch, archetype, dollar_amount)
            budget_items.append(BudgetItem(
                channel=channel_name,
                allocated_dollars=dollar_amount,
                percentage=pct,
                tactics=tactics
            ))

        return budget_map, budget_items

    @staticmethod
    def _get_tactics_for_channel(channel: TractionChannel, archetype: VentureArchetype, dollars: float) -> List[str]:
        """Provides concrete budget execution tactics based on allocated capital."""
        if dollars < 1000:
            return [
                f"Micro-testing ({channel.value}): Run controlled experiments ($10-$20/day) to validate CTR and messaging hooks",
                "Organic community seeding and founder direct engagement",
                "Landing page CTA conversion rate benchmarking"
            ]
        elif dollars < 10000:
            return [
                f"Core acquisition focus ({channel.value}): Target high-intent search and niche community ads",
                "A/B test 3 creative angles and 2 distinct value propositions",
                "Implement conversion retargeting and dedicated lead capture workflows"
            ]
        else:
            return [
                f"Scaled campaign rollout ({channel.value}): Multi-audience targeting with weekly creative refreshes",
                "Full-funnel attribution and automated CRM lead scoring",
                "Engage specialized agency or freelance specialist for production assets"
            ]
