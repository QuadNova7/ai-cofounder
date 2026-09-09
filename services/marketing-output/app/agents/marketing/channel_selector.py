"""Bullseye Channel Selector.

Evaluates Gabriel Weinberg's 19 Traction Channels using a multi-factor weighted
scoring rubric (Archetype 40%, Budget 30%, Price/ACV 15%, Founder Skills 15%)
and groups them into Inner Circle, Potential, and Long Shots.
"""

from typing import List, Dict, Optional
from shared.contracts.idea import IdeaAnalysisOutput, FounderInput
from shared.contracts.revenue import RevenueEstimationOutput
from app.agents.marketing.schemas import (
    VentureArchetype, TractionChannel, ChannelScore, BullseyeRanking
)


# Baseline suitability matrices per Archetype for all 19 channels (0.0 to 1.0)
ARCHETYPE_CHANNEL_FIT: Dict[VentureArchetype, Dict[TractionChannel, float]] = {
    VentureArchetype.B2B_SAAS: {
        TractionChannel.SALES: 0.95,
        TractionChannel.CONTENT_MARKETING: 0.90,
        TractionChannel.SEARCH_ENGINE_OPTIMIZATION: 0.85,
        TractionChannel.SEARCH_ENGINE_MARKETING: 0.80,
        TractionChannel.TRADE_SHOWS: 0.75,
        TractionChannel.SPEAKING_ENGAGEMENTS: 0.75,
        TractionChannel.EMAIL_MARKETING: 0.85,
        TractionChannel.TARGETING_BLOGS: 0.70,
        TractionChannel.BUSINESS_DEVELOPMENT: 0.75,
        TractionChannel.COMMUNITY_BUILDING: 0.65,
        TractionChannel.SOCIAL_AND_DISPLAY_ADS: 0.60,
        TractionChannel.ENGINEERING_AS_MARKETING: 0.65,
        TractionChannel.PUBLICITY: 0.55,
        TractionChannel.AFFILIATE_PROGRAMS: 0.40,
        TractionChannel.EXISTING_PLATFORMS: 0.50,
        TractionChannel.VIRAL_MARKETING: 0.35,
        TractionChannel.OFFLINE_EVENTS: 0.60,
        TractionChannel.UNCONVENTIONAL_PR: 0.30,
        TractionChannel.OFFLINE_ADS: 0.15,
    },
    VentureArchetype.PLG_DEVTOOLS: {
        TractionChannel.COMMUNITY_BUILDING: 0.95,
        TractionChannel.CONTENT_MARKETING: 0.95,
        TractionChannel.ENGINEERING_AS_MARKETING: 0.95,
        TractionChannel.EXISTING_PLATFORMS: 0.90,
        TractionChannel.SEARCH_ENGINE_OPTIMIZATION: 0.85,
        TractionChannel.VIRAL_MARKETING: 0.75,
        TractionChannel.TARGETING_BLOGS: 0.75,
        TractionChannel.EMAIL_MARKETING: 0.70,
        TractionChannel.PUBLICITY: 0.70,
        TractionChannel.SPEAKING_ENGAGEMENTS: 0.75,
        TractionChannel.BUSINESS_DEVELOPMENT: 0.60,
        TractionChannel.SEARCH_ENGINE_MARKETING: 0.50,
        TractionChannel.OFFLINE_EVENTS: 0.65,
        TractionChannel.SALES: 0.40,
        TractionChannel.SOCIAL_AND_DISPLAY_ADS: 0.40,
        TractionChannel.AFFILIATE_PROGRAMS: 0.35,
        TractionChannel.TRADE_SHOWS: 0.40,
        TractionChannel.UNCONVENTIONAL_PR: 0.40,
        TractionChannel.OFFLINE_ADS: 0.10,
    },
    VentureArchetype.B2C_MOBILE: {
        TractionChannel.VIRAL_MARKETING: 0.95,
        TractionChannel.SOCIAL_AND_DISPLAY_ADS: 0.90,
        TractionChannel.EXISTING_PLATFORMS: 0.95,  # App Stores
        TractionChannel.AFFILIATE_PROGRAMS: 0.85,
        TractionChannel.COMMUNITY_BUILDING: 0.80,
        TractionChannel.UNCONVENTIONAL_PR: 0.75,
        TractionChannel.PUBLICITY: 0.70,
        TractionChannel.EMAIL_MARKETING: 0.65,
        TractionChannel.TARGETING_BLOGS: 0.60,
        TractionChannel.SEARCH_ENGINE_OPTIMIZATION: 0.55,
        TractionChannel.SEARCH_ENGINE_MARKETING: 0.50,
        TractionChannel.ENGINEERING_AS_MARKETING: 0.50,
        TractionChannel.CONTENT_MARKETING: 0.45,
        TractionChannel.BUSINESS_DEVELOPMENT: 0.40,
        TractionChannel.OFFLINE_EVENTS: 0.35,
        TractionChannel.OFFLINE_ADS: 0.30,
        TractionChannel.SPEAKING_ENGAGEMENTS: 0.25,
        TractionChannel.SALES: 0.10,
        TractionChannel.TRADE_SHOWS: 0.15,
    },
    VentureArchetype.D2C_ECOMMERCE: {
        TractionChannel.SOCIAL_AND_DISPLAY_ADS: 0.95,
        TractionChannel.AFFILIATE_PROGRAMS: 0.90,
        TractionChannel.EMAIL_MARKETING: 0.90,
        TractionChannel.SEARCH_ENGINE_MARKETING: 0.85,
        TractionChannel.VIRAL_MARKETING: 0.80,
        TractionChannel.SEARCH_ENGINE_OPTIMIZATION: 0.75,
        TractionChannel.TARGETING_BLOGS: 0.70,
        TractionChannel.COMMUNITY_BUILDING: 0.65,
        TractionChannel.UNCONVENTIONAL_PR: 0.60,
        TractionChannel.CONTENT_MARKETING: 0.55,
        TractionChannel.PUBLICITY: 0.55,
        TractionChannel.BUSINESS_DEVELOPMENT: 0.50,
        TractionChannel.EXISTING_PLATFORMS: 0.50,
        TractionChannel.OFFLINE_ADS: 0.35,
        TractionChannel.OFFLINE_EVENTS: 0.30,
        TractionChannel.ENGINEERING_AS_MARKETING: 0.30,
        TractionChannel.TRADE_SHOWS: 0.25,
        TractionChannel.SPEAKING_ENGAGEMENTS: 0.20,
        TractionChannel.SALES: 0.10,
    },
    VentureArchetype.MARKETPLACE: {
        TractionChannel.SALES: 0.90,  # Direct supply recruitment
        TractionChannel.SEARCH_ENGINE_OPTIMIZATION: 0.90,
        TractionChannel.VIRAL_MARKETING: 0.85,
        TractionChannel.COMMUNITY_BUILDING: 0.80,
        TractionChannel.SEARCH_ENGINE_MARKETING: 0.80,
        TractionChannel.OFFLINE_EVENTS: 0.75,
        TractionChannel.PUBLICITY: 0.75,
        TractionChannel.EMAIL_MARKETING: 0.70,
        TractionChannel.SOCIAL_AND_DISPLAY_ADS: 0.70,
        TractionChannel.TARGETING_BLOGS: 0.65,
        TractionChannel.BUSINESS_DEVELOPMENT: 0.65,
        TractionChannel.CONTENT_MARKETING: 0.60,
        TractionChannel.UNCONVENTIONAL_PR: 0.55,
        TractionChannel.AFFILIATE_PROGRAMS: 0.50,
        TractionChannel.ENGINEERING_AS_MARKETING: 0.50,
        TractionChannel.EXISTING_PLATFORMS: 0.45,
        TractionChannel.TRADE_SHOWS: 0.35,
        TractionChannel.SPEAKING_ENGAGEMENTS: 0.35,
        TractionChannel.OFFLINE_ADS: 0.20,
    },
    VentureArchetype.DEEPTECH_HARDWARE: {
        TractionChannel.BUSINESS_DEVELOPMENT: 0.95,
        TractionChannel.TRADE_SHOWS: 0.90,
        TractionChannel.SPEAKING_ENGAGEMENTS: 0.90,
        TractionChannel.PUBLICITY: 0.85,
        TractionChannel.SALES: 0.80,
        TractionChannel.CONTENT_MARKETING: 0.75,
        TractionChannel.COMMUNITY_BUILDING: 0.70,
        TractionChannel.EMAIL_MARKETING: 0.60,
        TractionChannel.TARGETING_BLOGS: 0.55,
        TractionChannel.SEARCH_ENGINE_OPTIMIZATION: 0.50,
        TractionChannel.ENGINEERING_AS_MARKETING: 0.45,
        TractionChannel.EXISTING_PLATFORMS: 0.40,
        TractionChannel.SEARCH_ENGINE_MARKETING: 0.35,
        TractionChannel.OFFLINE_EVENTS: 0.40,
        TractionChannel.VIRAL_MARKETING: 0.30,
        TractionChannel.SOCIAL_AND_DISPLAY_ADS: 0.25,
        TractionChannel.UNCONVENTIONAL_PR: 0.25,
        TractionChannel.AFFILIATE_PROGRAMS: 0.20,
        TractionChannel.OFFLINE_ADS: 0.15,
    }
}

# Capital intensity of channels (minimum recommended budget score)
CHANNEL_BUDGET_REQUIREMENT = {
    TractionChannel.OFFLINE_ADS: 0.95,
    TractionChannel.TRADE_SHOWS: 0.80,
    TractionChannel.SOCIAL_AND_DISPLAY_ADS: 0.70,
    TractionChannel.SEARCH_ENGINE_MARKETING: 0.65,
    TractionChannel.PUBLICITY: 0.50,
    TractionChannel.OFFLINE_EVENTS: 0.50,
    TractionChannel.AFFILIATE_PROGRAMS: 0.45,
    TractionChannel.UNCONVENTIONAL_PR: 0.40,
    TractionChannel.SALES: 0.35,
    TractionChannel.EMAIL_MARKETING: 0.25,
    TractionChannel.TARGETING_BLOGS: 0.25,
    TractionChannel.CONTENT_MARKETING: 0.20,
    TractionChannel.SEARCH_ENGINE_OPTIMIZATION: 0.20,
    TractionChannel.BUSINESS_DEVELOPMENT: 0.20,
    TractionChannel.ENGINEERING_AS_MARKETING: 0.20,
    TractionChannel.SPEAKING_ENGAGEMENTS: 0.15,
    TractionChannel.COMMUNITY_BUILDING: 0.10,
    TractionChannel.EXISTING_PLATFORMS: 0.10,
    TractionChannel.VIRAL_MARKETING: 0.10,
}


class BullseyeChannelSelector:
    """Selects and ranks channels across Gabriel Weinberg's 19 Traction Channels."""

    @staticmethod
    def rank_channels(
        archetype: VentureArchetype,
        founder: Optional[FounderInput],
        revenue: Optional[RevenueEstimationOutput]
    ) -> BullseyeRanking:
        budget = founder.budget if founder else 0.0
        skills_text = (founder.skills_resources or "").lower() if founder else ""
        monthly_price = revenue.parameters.monthly_price if revenue and revenue.parameters else 50.0

        archetype_map = ARCHETYPE_CHANNEL_FIT.get(archetype, ARCHETYPE_CHANNEL_FIT[VentureArchetype.B2B_SAAS])
        scored_channels: List[ChannelScore] = []

        for ch in TractionChannel:
            arch_fit = archetype_map.get(ch, 0.50)

            # 1. Budget Feasibility Score (30%)
            cost_req = CHANNEL_BUDGET_REQUIREMENT.get(ch, 0.30)
            if budget <= 0.0:
                # Sweat equity mode: high cost channels penalized heavily
                budget_fit = 1.0 - cost_req
            elif budget < 2500.0:
                # Bootstrap mode
                budget_fit = 1.0 - (cost_req * 0.7)
            elif budget < 20000.0:
                # Seed mode: balanced
                budget_fit = 0.85
            else:
                # Well-funded: all channels financially viable
                budget_fit = 0.95

            # 2. ACV / Price Fit Score (15%)
            # High price favors Sales, Trade Shows, BD; Low price favors Viral, SEO, Ads
            if monthly_price >= 100.0:
                if ch in [TractionChannel.SALES, TractionChannel.BUSINESS_DEVELOPMENT, TractionChannel.TRADE_SHOWS, TractionChannel.SPEAKING_ENGAGEMENTS]:
                    acv_fit = 0.95
                elif ch in [TractionChannel.VIRAL_MARKETING, TractionChannel.AFFILIATE_PROGRAMS]:
                    acv_fit = 0.40
                else:
                    acv_fit = 0.75
            else:
                if ch in [TractionChannel.SALES, TractionChannel.TRADE_SHOWS]:
                    acv_fit = 0.35  # Direct sales unsustainable for $10/mo
                elif ch in [TractionChannel.VIRAL_MARKETING, TractionChannel.EXISTING_PLATFORMS, TractionChannel.SEARCH_ENGINE_OPTIMIZATION]:
                    acv_fit = 0.95
                else:
                    acv_fit = 0.70

            # 3. Founder Skills / Constraint Fit (15%)
            skills_fit = 0.65  # Neutral baseline
            if "technical" in skills_text or "developer" in skills_text or "code" in skills_text:
                if ch in [TractionChannel.ENGINEERING_AS_MARKETING, TractionChannel.EXISTING_PLATFORMS, TractionChannel.COMMUNITY_BUILDING, TractionChannel.SEARCH_ENGINE_OPTIMIZATION]:
                    skills_fit = 0.95
            if "sales" in skills_text or "network" in skills_text or "business" in skills_text:
                if ch in [TractionChannel.SALES, TractionChannel.BUSINESS_DEVELOPMENT, TractionChannel.SPEAKING_ENGAGEMENTS]:
                    skills_fit = 0.95
            if "marketing" in skills_text or "writer" in skills_text or "content" in skills_text:
                if ch in [TractionChannel.CONTENT_MARKETING, TractionChannel.EMAIL_MARKETING, TractionChannel.TARGETING_BLOGS]:
                    skills_fit = 0.95

            # Total Weighted Score
            total_score = round(
                (arch_fit * 0.40) +
                (budget_fit * 0.30) +
                (acv_fit * 0.15) +
                (skills_fit * 0.15),
                3
            )

            # Assign CAC Tier and Rationale
            cac_tier = "LOW ($0-$50)" if cost_req <= 0.30 else ("MEDIUM ($50-$250)" if cost_req <= 0.65 else "HIGH ($250-$1000+)")
            rationale = BullseyeChannelSelector._generate_rationale(ch, archetype, total_score, budget)

            scored_channels.append(ChannelScore(
                channel=ch,
                fit_score=total_score,
                archetype_fit=arch_fit,
                budget_fit=budget_fit,
                acv_fit=acv_fit,
                skills_fit=skills_fit,
                rationale=rationale,
                estimated_cac_tier=cac_tier
            ))

        # Sort descending by fit score
        scored_channels.sort(key=lambda x: x.fit_score, reverse=True)

        inner_circle = scored_channels[:3]
        potential = scored_channels[3:7]
        long_shots = scored_channels[7:]

        return BullseyeRanking(
            inner_circle=inner_circle,
            potential=potential,
            long_shots=long_shots
        )

    @staticmethod
    def _generate_rationale(channel: TractionChannel, archetype: VentureArchetype, score: float, budget: float) -> str:
        if score >= 0.80:
            return f"Optimal channel for {archetype.value}. High conversion efficiency aligned with early founder capital."
        elif score >= 0.65:
            return f"Viable secondary test channel once initial messaging and customer conversion are proven."
        elif budget <= 0.0 and CHANNEL_BUDGET_REQUIREMENT.get(channel, 0.0) >= 0.60:
            return "Requires upfront paid media or capital expenditure; ruled out during bootstrap zero-budget phase."
        else:
            return f"Low immediate ROI for {archetype.value}; deprioritized to preserve early runway."
