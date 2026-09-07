"""Business Intelligence Domain Strict Interface.

Exposes public entrypoints for Idea Analysis and RAG-powered Business Model Canvas synthesis.
All interactions from orchestrator or other agents must pass through this interface.
"""

from typing import Optional
from shared.contracts.idea import FounderInput, IdeaAnalysisOutput
from shared.contracts.market import MarketResearchOutput
from shared.contracts.business_model import BusinessModelOutput, BusinessModelCanvas


async def run_idea_analysis(founder_input: FounderInput) -> IdeaAnalysisOutput:
    """Deconstructs founder input into core assumptions, value proposition, and customer segments."""
    # In full implementation, delegates to app.agents.idea_analysis.agent
    return IdeaAnalysisOutput(
        refined_value_proposition=founder_input.value_proposition or f"Automated solution for {founder_input.target_audience}",
        target_customer_segments=[founder_input.target_audience] if founder_input.target_audience else ["General Innovators"],
        core_problem_statement=founder_input.problem_statement or "Streamline workflow inefficiencies",
        hypotheses_to_test=["Willingness to pay exists", "Market demand is scalable"],
        unfair_advantages=["Domain expertise", "First-mover speed"]
    )


async def run_business_model(
    idea: IdeaAnalysisOutput,
    market: MarketResearchOutput
) -> BusinessModelOutput:
    """Synthesizes the 9 Business Model Canvas blocks using ChromaDB RAG and market data."""
    # In full implementation, delegates to app.agents.business_model.agent with RAG retrieval
    canvas = BusinessModelCanvas(
        key_partners=["Cloud Providers", "Data Aggregators", "Distribution Channels"],
        key_activities=["Platform Development", "Algorithm Tuning", "Customer Success"],
        key_resources=["Proprietary AI Models", "Domain Knowledge Corpus", "Engineering Team"],
        value_propositions=[idea.refined_value_proposition],
        customer_relationships=["Automated Self-Serve", "Community Support"],
        channels=["Direct Web App", "Product-Led Growth", "Founder Networks"],
        customer_segments=idea.target_customer_segments,
        cost_structure=["Cloud Infrastructure", "API Costs", "Salaries"],
        revenue_streams=["Subscription Tiers (B2B SaaS)", "Usage-Based Add-ons"]
    )
    return BusinessModelOutput(
        canvas=canvas,
        framework_used="Osterwalder Business Model Canvas (BMC)",
        strategic_summary=f"Scalable B2B model focused on {', '.join(idea.target_customer_segments)}"
    )
