"""Venture Archetype Classifier.

Classifies early-stage startups into primary archetypes using deterministic
signals from problem statements, business model canvas, and pricing models.
"""

from typing import Optional
from shared.contracts.idea import IdeaAnalysisOutput, FounderInput
from shared.contracts.business_model import BusinessModelOutput
from shared.contracts.revenue import RevenueEstimationOutput
from app.agents.marketing.schemas import VentureArchetype


class ArchetypeClassifier:
    """Classifies startup ventures into actionable GTM archetypes."""

    @staticmethod
    def classify(
        idea: IdeaAnalysisOutput,
        business_model: Optional[BusinessModelOutput] = None,
        revenue: Optional[RevenueEstimationOutput] = None,
        founder: Optional[FounderInput] = None
    ) -> VentureArchetype:
        """Determines the venture archetype based on weighted keyword and contract heuristics."""
        text_corpus = " ".join([
            idea.problem_statement or "",
            idea.refined_value_proposition or "",
            " ".join(idea.target_users or []),
            founder.startup_idea if founder else "",
            founder.target_market if founder else "",
            revenue.pricing_strategy if revenue else "",
            " ".join(business_model.canvas.revenue_streams) if business_model and business_model.canvas else "",
            " ".join(business_model.canvas.channels) if business_model and business_model.canvas else "",
        ]).lower()

        monthly_price = revenue.parameters.monthly_price if revenue and revenue.parameters else 0.0

        # Heuristic Scores
        scores = {
            VentureArchetype.PLG_DEVTOOLS: 0,
            VentureArchetype.B2B_SAAS: 0,
            VentureArchetype.MARKETPLACE: 0,
            VentureArchetype.B2C_MOBILE: 0,
            VentureArchetype.D2C_ECOMMERCE: 0,
            VentureArchetype.DEEPTECH_HARDWARE: 0,
        }

        # 1. DevTools & PLG Signals
        for kw in ["developer", "developers", "devtools", "api", "sdk", "github", "open-source", "open source", "cli", "code", "devops", "engineers"]:
            if kw in text_corpus:
                scores[VentureArchetype.PLG_DEVTOOLS] += 3

        # 2. Marketplace Signals
        for kw in ["marketplace", "two-sided", "platform", "buyers and sellers", "matching", "supply and demand", "take rate", "commission"]:
            if kw in text_corpus:
                scores[VentureArchetype.MARKETPLACE] += 4

        # 3. D2C E-commerce Signals
        for kw in ["ecommerce", "e-commerce", "d2c", "apparel", "physical product", "shopify", "shipping", "inventory", "brand", "retail"]:
            if kw in text_corpus:
                scores[VentureArchetype.D2C_ECOMMERCE] += 4

        # 4. DeepTech & Hardware Signals
        for kw in ["hardware", "iot", "robotics", "biotech", "sensor", "device", "patented", "deeptech", "semiconductor"]:
            if kw in text_corpus:
                scores[VentureArchetype.DEEPTECH_HARDWARE] += 4

        # 5. B2C Consumer Signals
        for kw in ["consumer", "mobile app", "ios", "android", "social network", "fitness app", "personal finance", "daily habit", "gamified"]:
            if kw in text_corpus:
                scores[VentureArchetype.B2C_MOBILE] += 3
        if 0 < monthly_price < 25.0:
            scores[VentureArchetype.B2C_MOBILE] += 2

        # 6. B2B SaaS Signals
        for kw in ["b2b", "enterprise", "teams", "workflow", "crm", "compliance", "procurement", "dashboard", "collaboration", "saas", "b2b saas"]:
            if kw in text_corpus:
                scores[VentureArchetype.B2B_SAAS] += 3
        if monthly_price >= 49.0:
            scores[VentureArchetype.B2B_SAAS] += 3

        # Default fallback
        best_archetype = max(scores, key=scores.get)
        if scores[best_archetype] == 0:
            # Baseline based on price or general B2B vs B2C
            if monthly_price >= 40.0:
                return VentureArchetype.B2B_SAAS
            return VentureArchetype.PLG_DEVTOOLS

        return best_archetype
