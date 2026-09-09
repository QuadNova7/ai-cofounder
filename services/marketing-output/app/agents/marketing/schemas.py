"""Marketing Domain Schemas & Enums.

Defines domain-specific data structures for the Bullseye Framework,
Venture Archetypes, Unit Economics, and 12-Week GTM Sprints.
"""

from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class VentureArchetype(str, Enum):
    """Core venture classification driving GTM strategy."""
    B2B_SAAS = "B2B Enterprise SaaS"
    PLG_DEVTOOLS = "Product-Led Growth & DevTools"
    B2C_MOBILE = "B2C Consumer & Mobile"
    D2C_ECOMMERCE = "D2C & E-Commerce"
    MARKETPLACE = "Two-Sided Marketplace"
    DEEPTECH_HARDWARE = "DeepTech & Hardware"


class TractionChannel(str, Enum):
    """Gabriel Weinberg's 19 Traction Channels (Bullseye Framework)."""
    TARGETING_BLOGS = "Targeting Blogs"
    PUBLICITY = "Publicity & PR"
    UNCONVENTIONAL_PR = "Unconventional PR"
    SEARCH_ENGINE_MARKETING = "Search Engine Marketing (SEM / Search Ads)"
    SOCIAL_AND_DISPLAY_ADS = "Social & Display Advertising"
    OFFLINE_ADS = "Offline Advertising"
    SEARCH_ENGINE_OPTIMIZATION = "Search Engine Optimization (SEO)"
    CONTENT_MARKETING = "Content Marketing & Thought Leadership"
    EMAIL_MARKETING = "Email & Lifecycle Marketing"
    ENGINEERING_AS_MARKETING = "Engineering as Marketing (Free Tools / Widgets)"
    VIRAL_MARKETING = "Viral Marketing & Referral Loops"
    BUSINESS_DEVELOPMENT = "Business Development & Strategic Partnerships"
    SALES = "Direct Sales & Cold Outbound"
    AFFILIATE_PROGRAMS = "Affiliate & Influencer Programs"
    EXISTING_PLATFORMS = "Existing Platforms (App Store, GitHub, Chrome Web Store)"
    TRADE_SHOWS = "Trade Shows & Industry Events"
    OFFLINE_EVENTS = "Offline Events & Meetups"
    SPEAKING_ENGAGEMENTS = "Speaking Engagements & Podcasts"
    COMMUNITY_BUILDING = "Community Building (Discord, Reddit, Slack)"


class ChannelScore(BaseModel):
    """Evaluation score for a traction channel."""
    channel: TractionChannel
    fit_score: float = Field(ge=0.0, le=1.0, description="Overall weighted fit score 0.0 to 1.0")
    archetype_fit: float
    budget_fit: float
    acv_fit: float
    skills_fit: float
    rationale: str
    estimated_cac_tier: str  # "LOW ($0-$50)", "MEDIUM ($50-$250)", "HIGH ($250-$1000+)"


class BullseyeRanking(BaseModel):
    """Bullseye Framework 3-ring classification."""
    inner_circle: List[ChannelScore] = Field(description="Top 3 priority channels to test first")
    potential: List[ChannelScore] = Field(description="Secondary channels for expansion in Month 2/3")
    long_shots: List[ChannelScore] = Field(description="Ruled-out or unviable channels with rationale")


class UnitEconomicsMetrics(BaseModel):
    """Deterministic financial metrics governing customer acquisition."""
    monthly_price: float
    monthly_churn_rate: float
    estimated_ltv: float
    target_cac: float
    cac_payback_months: float
    ltv_cac_ratio: float


class BudgetItem(BaseModel):
    """Allocated budget for an acquisition channel."""
    channel: str
    allocated_dollars: float
    percentage: float
    tactics: List[str]


class WeeklySprintItem(BaseModel):
    """A single weekly sprint within the 90-day (12-week) execution plan."""
    week: int = Field(ge=1, le=12)
    month: int = Field(ge=1, le=3)
    focus: str
    target_kpi: str
    deliverables: List[str]


class MarketingAgentResult(BaseModel):
    """Internal consolidated result from Marketing Agent before contract serialization."""
    archetype: VentureArchetype
    positioning_statement: str
    messaging_framework: Dict[str, str]
    bullseye: BullseyeRanking
    unit_economics: UnitEconomicsMetrics
    budget_items: List[BudgetItem]
    weekly_sprints: List[WeeklySprintItem]
    prioritized_next_actions: List[str]
    acquisition_tactics: List[str]
    warnings: List[str] = Field(default_factory=list)
