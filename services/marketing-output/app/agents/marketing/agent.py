"""Marketing Agent.

Orchestrates venture archetype classification, Bullseye traction channel selection,
deterministic unit economics & budget math, and 12-week GTM launch roadmap generation.
"""

import json
from typing import Optional, List, Dict, Any
from shared.contracts.idea import IdeaAnalysisOutput, FounderInput
from shared.contracts.market import MarketResearchOutput
from shared.contracts.business_model import BusinessModelOutput
from shared.contracts.revenue import RevenueEstimationOutput
from shared.contracts.marketing import MarketingPlanOutput, Milestone

from app.agents.marketing.schemas import (
    VentureArchetype, TractionChannel, ChannelScore, BullseyeRanking,
    UnitEconomicsMetrics, BudgetItem
)
from app.agents.marketing.archetypes import ArchetypeClassifier
from app.agents.marketing.channel_selector import BullseyeChannelSelector
from app.agents.marketing.budget_allocator import DeterministicBudgetAllocator
from app.agents.marketing.fallback_templates import get_fallback_plan
from app.agents.marketing.gtm_plan import GTMPlanGenerator
from app.agents.marketing.prompts import (
    SYSTEM_MARKETING_PROMPT, build_marketing_user_prompt
)


class MarketingAgent:
    """Autonomous Marketing & GTM Strategy Agent."""

    def __init__(self, llm_client: Optional[Any] = None):
        self.llm_client = llm_client

    def generate_plan(
        self,
        idea: IdeaAnalysisOutput,
        market: MarketResearchOutput,
        business_model: BusinessModelOutput,
        revenue: RevenueEstimationOutput,
        founder: Optional[FounderInput] = None
    ) -> MarketingPlanOutput:
        """Executes the two-phase hybrid GTM formulation pipeline."""
        warnings: List[str] = []

        # -------------------------------------------------------------
        # 1. Venture Archetype Classification (Deterministic)
        # -------------------------------------------------------------
        archetype = ArchetypeClassifier.classify(
            idea=idea,
            business_model=business_model,
            revenue=revenue,
            founder=founder
        )

        # -------------------------------------------------------------
        # 2. Bullseye Traction Channel Selection (19 Channels Weighted)
        # -------------------------------------------------------------
        bullseye = BullseyeChannelSelector.rank_channels(
            archetype=archetype,
            founder=founder,
            revenue=revenue
        )
        priority_channels_enum = [c.channel for c in bullseye.inner_circle]
        priority_channels_names = [c.channel.value for c in bullseye.inner_circle]

        # -------------------------------------------------------------
        # 3. Deterministic Unit Economics & Budget Math
        # -------------------------------------------------------------
        unit_econ = DeterministicBudgetAllocator.calculate_unit_economics(revenue)
        total_budget = founder.budget if founder else 0.0
        budget_map, budget_items = DeterministicBudgetAllocator.allocate_budget(
            total_budget=total_budget,
            archetype=archetype,
            priority_channels=priority_channels_enum
        )

        # -------------------------------------------------------------
        # 4. Qualitative Positioning & Sprints (LLM with Robust Fallback)
        # -------------------------------------------------------------
        llm_result = None
        if self.llm_client:
            try:
                prompt_channels = "\n".join([
                    f"- {c.channel.value}: {c.rationale} (Fit Score: {c.fit_score})"
                    for c in bullseye.inner_circle
                ])
                user_prompt = build_marketing_user_prompt(
                    archetype_name=archetype.value,
                    idea_summary=idea.refined_value_proposition or idea.problem_statement,
                    target_segments=", ".join(idea.target_users or ["General users"]),
                    competitors=", ".join([c.name for c in market.competitor_landscape[:3]]) if market and market.competitor_landscape else "Direct alternatives",
                    channels=prompt_channels,
                    pricing_model=revenue.pricing_strategy if revenue else "Subscription",
                    budget=total_budget,
                    founder_skills=founder.skills_resources if founder else "",
                    constraints=", ".join(founder.constraints) if founder and founder.constraints else ""
                )

                if hasattr(self.llm_client, "generate_json"):
                    llm_result = self.llm_client.generate_json(
                        prompt=f"{SYSTEM_MARKETING_PROMPT}\n\n{user_prompt}",
                        schema=None
                    )
            except Exception as e:
                warnings.append(f"LLM generation failed ({str(e)}); falling back to deterministic template.")
                llm_result = None

        # Engage Fallback if LLM output is absent or missing critical keys
        if not llm_result or not isinstance(llm_result, dict) or "weekly_sprints" not in llm_result:
            if self.llm_client and not warnings:
                warnings.append("LLM returned incomplete schema; engaged deterministic archetype template.")
            template = get_fallback_plan(archetype)
            
            positioning = (
                f"For {', '.join(idea.target_users or ['modern teams'])}, our platform delivers "
                f"{idea.refined_value_proposition or 'exceptional efficiency'}. Unlike traditional alternatives, "
                f"we combine rapid onboarding with verifiable ROI."
            )
            messaging_framework = template["messaging_framework"]
            acquisition_tactics = template["acquisition_tactics"]
            prioritized_next_actions = template["prioritized_next_actions"]
            raw_sprints = template["weekly_sprints"]
        else:
            positioning = llm_result.get(
                "positioning_statement",
                f"For {', '.join(idea.target_users or ['innovative teams'])}, our platform delivers {idea.refined_value_proposition}."
            )
            messaging_framework = llm_result.get("messaging_framework", {})
            acquisition_tactics = llm_result.get("acquisition_tactics", [])
            prioritized_next_actions = llm_result.get("prioritized_next_actions", [])
            raw_sprints = llm_result.get("weekly_sprints", [])

        # -------------------------------------------------------------
        # 5. Build Typed 12-Week Milestones
        # -------------------------------------------------------------
        milestones = GTMPlanGenerator.build_milestones_from_sprints(raw_sprints)

        # -------------------------------------------------------------
        # 6. Assemble Final MarketingPlanOutput Contract
        # -------------------------------------------------------------
        return MarketingPlanOutput(
            positioning_statement=positioning,
            priority_channels=priority_channels_names,
            messaging_framework=messaging_framework,
            gtm_90_day_plan=milestones,
            acquisition_tactics=acquisition_tactics,
            budget_allocation=budget_map,
            prioritized_next_actions=prioritized_next_actions,
            venture_archetype=archetype.value,
            target_cac=unit_econ.target_cac,
            estimated_ltv=unit_econ.estimated_ltv,
            cac_payback_months=unit_econ.cac_payback_months,
            budget_breakdown_dollars=budget_map,
            warnings=warnings
        )
