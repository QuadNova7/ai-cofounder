"""Curated Deterministic Marketing Templates.

Provides high-fidelity fallback plans per Venture Archetype if LLM generation
times out, errors, or is not configured.
"""

from typing import Dict, List
from app.agents.marketing.schemas import VentureArchetype, WeeklySprintItem


ARCHETYPE_TEMPLATES: Dict[VentureArchetype, Dict] = {
    VentureArchetype.B2B_SAAS: {
        "messaging_framework": {
            "headline": "Modern Workflow Intelligence Built for High-Growth Teams",
            "subheadline": "Eliminate operational friction and manual silos with deterministic execution.",
            "elevator_pitch": "An enterprise-grade platform that automates core operational workflows, delivering measurable ROI within 30 days.",
            "proof_points": "Deterministic accuracy, SOC2 compliance ready, verified customer case benchmarks.",
            "primary_cta": "Book a 15-Minute Technical Demo"
        },
        "acquisition_tactics": [
            "Cold outreach to targeted ICP titles on LinkedIn with personalized workflow audits",
            "High-intent bottom-of-funnel comparison articles ('X vs Competitor Y')",
            "Bi-weekly live webinars demonstrating solution workflows with Q&A",
            "Automated interactive product tours (Navattic/Storylane) embedded on homepage"
        ],
        "prioritized_next_actions": [
            "Build high-converting landing page with interactive demo and waitlist capture",
            "Curate list of top 50 ICP target accounts on LinkedIn Sales Navigator",
            "Conduct 10 customer discovery interviews to validate painful workflow bottlenecks",
            "Set up domain authentication (DKIM, SPF, DMARC) for cold email deliverability"
        ],
        "weekly_sprints": [
            WeeklySprintItem(week=1, month=1, focus="ICP Definition & Messaging Validation", target_kpi="10 founder interviews booked", deliverables=["Refined ICP persona sheet", "Cold email copy deck (3 variants)", "Discovery call script"]),
            WeeklySprintItem(week=2, month=1, focus="Landing Page & Tracking Architecture", target_kpi="Landing page live with <2s load", deliverables=["High-converting hero section", "PostHog event tracking", "Waitlist calendar integration"]),
            WeeklySprintItem(week=3, month=1, focus="Private Alpha Outreach", target_kpi="5 active pilot teams onboarded", deliverables=["50 personalized LinkedIn messages", "Private Slack/Discord sandbox", "Onboarding checklist"]),
            WeeklySprintItem(week=4, month=1, focus="Alpha Feedback & Product Tuning", target_kpi="NPS > 40 from alpha cohort", deliverables=["Feedback survey analysis", "Top 3 critical bug fixes", "Initial customer quote capture"]),
            WeeklySprintItem(week=5, month=2, focus="Public Beta Launch Preparation", target_kpi="Product Hunt teaser live, 100 subscribers", deliverables=["Product Hunt assets & thumbnail", "Launch tweet thread & demo video", "Founder newsletter draft"]),
            WeeklySprintItem(week=6, month=2, focus="Public Launch Day & Community Push", target_kpi="Top 5 on Product Hunt, 250 signups", deliverables=["Community mobilization across Slack/Reddit", "Live launch day support", "Press release distribution"]),
            WeeklySprintItem(week=7, month=2, focus="Inbound Content Engine Spin-up", target_kpi="2 comparison articles published", deliverables=["'Alternative to [Incumbent]' article", "Technical architecture breakdown", "SEO keyword tracking"]),
            WeeklySprintItem(week=8, month=2, focus="Sales Pipeline & Demo Funnel", target_kpi="15 qualified demo calls held", deliverables=["HubSpot CRM deal stages", "Automated demo reminder sequence", "1-page product battlecard"]),
            WeeklySprintItem(week=9, month=3, focus="Self-Serve Billing & Monetization", target_kpi="First 5 paying subscribers", deliverables=["Stripe billing integration", "Pricing tiers UI", "Annual discount incentive banner"]),
            WeeklySprintItem(week=10, month=3, focus="High-Intent Paid Search Testing", target_kpi="CAC < $150 on Google Search", deliverables=["Google Ads campaign with 15 exact-match keywords", "Negative keyword list", "Dedicated landing page variant"]),
            WeeklySprintItem(week=11, month=3, focus="Customer Case Study Publication", target_kpi="1 comprehensive case study live", deliverables=["Customer ROI interview recording", "Published PDF and web case study", "Sales enablement PDF"]),
            WeeklySprintItem(week=12, month=3, focus="90-Day GTM Audit & Scaling Plan", target_kpi="LTV:CAC > 3.0, Payback < 6 mo", deliverables=["Channel ROI audit dashboard", "Quarterly growth roadmap", "Hiring plan for first Growth Marketer"])
        ]
    },
    VentureArchetype.PLG_DEVTOOLS: {
        "messaging_framework": {
            "headline": "The Developer-First Engine for Rapid Innovation",
            "subheadline": "Open, extensible, and lightning-fast tooling designed by engineers, for engineers.",
            "elevator_pitch": "Empowering developers to build, test, and ship complex systems with intuitive CLI and APIs.",
            "proof_points": "Open-source core, zero lock-in, active Discord community, 1-command install.",
            "primary_cta": "Get Started in 60 Seconds (npm/pip install)"
        },
        "acquisition_tactics": [
            "Open-source core repo on GitHub with exceptional README and quickstart guide",
            "Interactive WebAssembly / browser playground allowing instant zero-install trials",
            "Technical tutorials and engineering deep-dives shared on Hacker News and dev.to",
            "Active developer office hours and troubleshooting support inside Discord"
        ],
        "prioritized_next_actions": [
            "Polish GitHub README with interactive GIF demonstration and benchmark table",
            "Deploy interactive web playground for friction-free evaluation",
            "Share 'Show HN' post on Hacker News with transparent technical design writeup",
            "Create starter template repos for Next.js, FastAPI, and Docker"
        ],
        "weekly_sprints": [
            WeeklySprintItem(week=1, month=1, focus="Developer DX & Quickstart Polish", target_kpi="Time-to-first-hello-world < 3 mins", deliverables=["Interactive README.md", "Copy-pasteable CLI commands", "Troubleshooting FAQ"]),
            WeeklySprintItem(week=2, month=1, focus="Interactive Playground Deployment", target_kpi="Live web sandbox with zero sign-up", deliverables=["Web playground hosted on Vercel", "Sample project templates", "One-click fork button"]),
            WeeklySprintItem(week=3, month=1, focus="Developer Beta Outreach", target_kpi="25 active developers in Discord", deliverables=["Personal invites to 40 open-source contributors", "Discord community setup", "Issue template on GitHub"]),
            WeeklySprintItem(week=4, month=1, focus="DX Refinement & Bug Squashing", target_kpi="Zero P0 issues on initial onboarding", deliverables=["Telemetry for CLI command dropoffs", "Automated error logging", "v0.2 release notes"]),
            WeeklySprintItem(week=5, month=2, focus="Hacker News 'Show HN' Launch", target_kpi="100+ points on Show HN, 500 stars", deliverables=["Show HN technical submission", "Architecture deep dive blog post", "Real-time comment engagement"]),
            WeeklySprintItem(week=6, month=2, focus="Product Hunt & Dev Directory Blitz", target_kpi="#1 Developer Tool of the Day", deliverables=["Product Hunt launch assets", "Listing on AlternativeTo and DevHunt", "Product launch video demo"]),
            WeeklySprintItem(week=7, month=2, focus="Technical Content & SEO Engine", target_kpi="1,000 unique blog readers", deliverables=["'How we built X in Rust/Python' article", "Benchmark comparison vs standard tooling", "Dev.to cross-posting"]),
            WeeklySprintItem(week=8, month=2, focus="Integration & Ecosystem Partnerships", target_kpi="3 official ecosystem integrations", deliverables=["Official VS Code extension or plugin", "GitHub Actions workflow template", "Partner co-marketing blog"]),
            WeeklySprintItem(week=9, month=3, focus="Team Tier / Cloud Hosted Beta", target_kpi="10 teams on cloud waitlist", deliverables=["Cloud dashboard prototype", "Team role management UI", "Pricing preview page"]),
            WeeklySprintItem(week=10, month=3, focus="Engineering-as-Marketing Tools", target_kpi="500 monthly tool users", deliverables=["Free online config validator / benchmark tool", "SEO landing page for validator", "Lead magnet export"]),
            WeeklySprintItem(week=11, month=3, focus="Community Showcase & Hackathon", target_kpi="15 community projects submitted", deliverables=["Virtual mini-hackathon announcement", "Prize pool & swag logistics", "Project showcase page"]),
            WeeklySprintItem(week=12, month=3, focus="Monetization Rollout & Cloud GA", target_kpi="First $1,000 MRR from developer teams", deliverables=["Cloud self-serve checkout", "Usage-based tier metering", "Enterprise support package tier"])
        ]
    },
    VentureArchetype.B2C_MOBILE: {
        "messaging_framework": {
            "headline": "Transform Your Daily Routine in Just 5 Minutes a Day",
            "subheadline": "The delightfully simple mobile companion designed to help you thrive.",
            "elevator_pitch": "A mobile application delivering immediate personal value with gamified habits and positive feedback loops.",
            "proof_points": "Rated 4.8 stars by early testers, privacy-first, zero intrusive advertisements.",
            "primary_cta": "Download Free on iOS & Android"
        },
        "acquisition_tactics": [
            "Short-form video UGC on TikTok and Instagram Reels showing before/after transformation",
            "App Store Optimization (ASO) targeting high-intent everyday search keywords",
            "Double-sided viral referral program ('Invite a friend, unlock Premium for 1 month')",
            "Micro-influencer gifting with fitness/productivity content creators"
        ],
        "prioritized_next_actions": [
            "Create App Store & Google Play product page screenshots and preview video",
            "Produce 5 native short-form TikTok/Reels videos highlighting core 'Aha!' moment",
            "Implement in-app viral referral button with dynamic deep links",
            "Launch TestFlight beta with 50 targeted early testers"
        ],
        "weekly_sprints": [
            WeeklySprintItem(week=1, month=1, focus="TestFlight Beta & Onboarding UX", target_kpi="D1 retention > 50% in beta", deliverables=["TestFlight build distribution", "Interactive onboarding flow", "Feedback questionnaire"]),
            WeeklySprintItem(week=2, month=1, focus="App Store Optimization (ASO)", target_kpi="ASO keyword score > 80", deliverables=["100 keyword list analyzed", "Localized store descriptions", "High-contrast screenshot set"]),
            WeeklySprintItem(week=3, month=1, focus="Organic Short-Form Video Creation", target_kpi="5 TikTok videos published, 10k views", deliverables=["5 scripted UGC hooks", "Video editing with trending audio", "TikTok/Reels account setup"]),
            WeeklySprintItem(week=4, month=1, focus="Pre-Order / Pre-Registration Push", target_kpi="500 App Store pre-orders", deliverables=["App Store pre-order page live", "Landing page with SMS/Email alert", "Social proof teasers"]),
            WeeklySprintItem(week=5, month=2, focus="Public App Store Launch Day", target_kpi="1,000 Day-1 installs", deliverables=["App release live globally", "Launch announcement across all channels", "Early reviewer activation push"]),
            WeeklySprintItem(week=6, month=2, focus="Viral Referral Loop Activation", target_kpi="Viral coefficient K > 0.35", deliverables=["In-app shareable milestone cards", "Dynamic invite links", "Reward tracking engine"]),
            WeeklySprintItem(week=7, month=2, focus="Micro-Influencer Gifting Wave", target_kpi="10 creator reviews published", deliverables=["Outreach to 30 niche TikTok/IG creators", "Free VIP code distribution", "UGC reposting permissions"]),
            WeeklySprintItem(week=8, month=2, focus="Push Notification & Retention Tuning", target_kpi="D7 retention > 25%", deliverables=["Smart behavioral push triggers", "Re-engagement message series", "Weekly progress recap card"]),
            WeeklySprintItem(week=9, month=3, focus="Paywall & Subscription Optimization", target_kpi="3.5% free-to-paid conversion", deliverables=["A/B test annual vs monthly paywall", "Trial ending reminder notification", "Stripe/Apple in-app purchase audit"]),
            WeeklySprintItem(week=10, month=3, focus="Paid User Acquisition Testing", target_kpi="CPI < $1.80 on Meta / Apple Search Ads", deliverables=["Apple Search Ads brand campaign", "Meta Advantage+ creative test", "ROAS tracking dashboard"]),
            WeeklySprintItem(week=11, month=3, focus="Community Challenges & Gamification", target_kpi="30% increase in daily active users", deliverables=["14-day user streak challenge", "Community leaderboard", "Custom completion badges"]),
            WeeklySprintItem(week=12, month=3, focus="App Store Feature Pitch & Scaling", target_kpi="Apple App Store editorial pitch sent", deliverables=["Editorial feature submission deck", "Quarterly growth metrics review", "Feature roadmap for v2.0"])
        ]
    },
    VentureArchetype.MARKETPLACE: {
        "messaging_framework": {
            "headline": "The Trusted Marketplace Connecting Buyers with Top-Tier Providers",
            "subheadline": "Transparent pricing, verified ratings, and guaranteed satisfaction on every transaction.",
            "elevator_pitch": "A curated two-sided platform solving fragmented industry discovery through seamless booking and trust.",
            "proof_points": "100% verified supply partners, escrow payments, dispute guarantee.",
            "primary_cta": "Explore Top Providers / Join as a Seller"
        },
        "acquisition_tactics": [
            "Manual supply recruitment: cold calling and onboarding the first 30 top-rated local providers",
            "Hyper-local geographic launch: dominate a single neighborhood or niche category first",
            "High-intent programmatic SEO pages ('Best [Service] in [City]')",
            "Double-sided referral incentives ($20 credit for both referrer and new customer)"
        ],
        "prioritized_next_actions": [
            "Manually recruit and onboard 20 anchor supply providers with verified profiles",
            "Launch geo-targeted landing page for initial launch territory",
            "Create programmatic SEO directory template for local service searches",
            "Establish guarantee policy and terms of service to build buyer trust"
        ],
        "weekly_sprints": [
            WeeklySprintItem(week=1, month=1, focus="Supply-Side Direct Recruitment", target_kpi="15 verified supply partners signed", deliverables=["Supplier pitch deck & pricing one-pager", "Concierge onboarding script", "Supplier profile templates"]),
            WeeklySprintItem(week=2, month=1, focus="Supply Liquidity & Onboarding", target_kpi="30 active listings populated", deliverables=["High-quality photography/assets for supply", "Calendar availability setup", "Stripe Connect payout onboarding"]),
            WeeklySprintItem(week=3, month=1, focus="Marketplace Trust Architecture", target_kpi="100% supply verified badges", deliverables=["Review & rating system", "Dispute resolution policy", "Customer protection badge"]),
            WeeklySprintItem(week=4, month=1, focus="Private Alpha Transaction Testing", target_kpi="10 test transactions completed", deliverables=["Friends & family test bookings", "Checkout friction audit", "Payment reconciliation test"]),
            WeeklySprintItem(week=5, month=2, focus="Hyper-Local Demand Launch", target_kpi="50 buyer signups in primary territory", deliverables=["Local community flyers / neighborhood ads", "Local Facebook group engagement", "$20 first-order voucher campaign"]),
            WeeklySprintItem(week=6, month=2, focus="Programmatic SEO Directory Spin-up", target_kpi="25 local landing pages indexed", deliverables=["Dynamic city/category directory templates", "Structured schema markup for reviews", "Local Google My Business page"]),
            WeeklySprintItem(week=7, month=2, focus="Buyer Repeat Rate Optimization", target_kpi="20% repeat booking within 30 days", deliverables=["Automated post-service review request", "Re-booking discount prompt via email", "Loyalty stamp program"]),
            WeeklySprintItem(week=8, month=2, focus="Supply Referral Program", target_kpi="5 new suppliers referred by current", deliverables=["Supplier referral bounty program ($100)", "Supplier dashboard banner", "Co-branded partner badges"]),
            WeeklySprintItem(week=9, month=3, focus="Take Rate & Monetization Polish", target_kpi="Gross Merchandise Value (GMV) > $10k", deliverables=["Automated commission deduction", "Featured listing sponsored placement tier", "Instant payout fee option"]),
            WeeklySprintItem(week=10, month=3, focus="High-Intent Local Search Ads", target_kpi="CAC < $35 per completed transaction", deliverables=["Google Local Services Ads setup", "Exact match search ads for top 3 categories", "Negative keyword tuning"]),
            WeeklySprintItem(week=11, month=3, focus="Expansion to Territory 2", target_kpi="10 supply partners in new zip code", deliverables=["Territory expansion playbook", "Replicated geo landing pages", "Cross-city promotion campaign"]),
            WeeklySprintItem(week=12, month=3, focus="Marketplace Liquidity Review", target_kpi="Match rate > 85%, Fill time < 2 hours", deliverables=["Quarterly GMV & take-rate audit", "Supply utilization report", "Seed round investor deck traction slide"])
        ]
    },
    VentureArchetype.D2C_ECOMMERCE: {
        "messaging_framework": {
            "headline": "Crafted for Everyday Excellence, Delivered Directly to You",
            "subheadline": "Premium quality without the retail markup. Sustainably sourced and built to last.",
            "elevator_pitch": "A modern consumer lifestyle brand delivering superior products directly to customers.",
            "proof_points": "30-day risk-free trial, free shipping over $50, 10,000+ happy customers.",
            "primary_cta": "Shop the Collection"
        },
        "acquisition_tactics": [
            "High-converting Meta & TikTok video ads emphasizing unboxing and texture/feel",
            "Klaviyo automated email/SMS flows (Welcome series, Abandoned cart, Post-purchase upsell)",
            "Creator product gifting to micro-influencers with dedicated discount codes",
            "Google Shopping & Performance Max campaigns for high-intent search"
        ],
        "prioritized_next_actions": [
            "Set up Shopify store with fast mobile checkout and trust badges",
            "Record 3 high-resolution unboxing and product lifestyle video ads",
            "Configure Klaviyo 3-step abandoned cart email and SMS flow",
            "Ship sample product kits to 15 targeted aesthetic creators"
        ],
        "weekly_sprints": [
            WeeklySprintItem(week=1, month=1, focus="Store UX & Conversion Architecture", target_kpi="Store checkout conversion > 3%", deliverables=["Shopify theme optimization", "One-click Apple Pay/Shop Pay setup", "Product page customer review widget"]),
            WeeklySprintItem(week=2, month=1, focus="Email & SMS Flow Setup", target_kpi="30% open rate on welcome series", deliverables=["Klaviyo welcome flow with 10% off code", "3-step abandoned cart recovery", "Post-purchase delivery tracking email"]),
            WeeklySprintItem(week=3, month=1, focus="Creative Asset Production", target_kpi="10 UGC ad creatives produced", deliverables=["3 hook-style unboxing videos", "5 aesthetic product lifestyle photos", "Customer quote overlay graphics"]),
            WeeklySprintItem(week=4, month=1, focus="Friends & Family VIP Launch", target_kpi="First 25 orders fulfilled", deliverables=["VIP secret link access", "Unboxing experience feedback check", "Shipping & packaging stress test"]),
            WeeklySprintItem(week=5, month=2, focus="Public Launch & Ad Campaign Start", target_kpi="ROAS > 2.0 on initial $500 ad spend", deliverables=["Meta Advantage+ Shopping campaign", "TikTok top-of-funnel creative test", "Conversion tracking pixel audit"]),
            WeeklySprintItem(week=6, month=2, focus="Micro-Influencer Gifting Wave", target_kpi="8 creator unboxing posts live", deliverables=["Creator outreach tracker", "Personalized affiliate discount codes", "Story reposting on brand channel"]),
            WeeklySprintItem(week=7, month=2, focus="Google Shopping & PMax Activation", target_kpi="Google ad ROAS > 3.0", deliverables=["Google Merchant Center product feed", "Performance Max campaign setup", "Negative search term filters"]),
            WeeklySprintItem(week=8, month=2, focus="Average Order Value (AOV) Boost", target_kpi="AOV increased by 15%", deliverables=["In-cart product recommendations", "'Free shipping over $60' threshold bar", "Bundle & Save product duo"]),
            WeeklySprintItem(week=9, month=3, focus="Customer Retention & Repeat Order Flow", target_kpi="15% 60-day repeat purchase rate", deliverables=["Replenishment reminder email flow", "VIP customer loyalty perks", "Customer feedback NPS survey"]),
            WeeklySprintItem(week=10, month=3, focus="Ad Creative Refresh & Scaling", target_kpi="Weekly ad spend scaled 2x sustainably", deliverables=["5 new hook variations tested", "Winning ad creative iteration", "Lookalike audience test"]),
            WeeklySprintItem(week=11, month=3, focus="Seasonal Promotion / Flash Sale", target_kpi="2x daily order volume spike", deliverables=["Limited-time promotion banner", "SMS flash sale broadcast", "Social media countdown teasers"]),
            WeeklySprintItem(week=12, month=3, focus="Quarterly E-Commerce Review", target_kpi="Gross margin > 65%, Blended CAC profitable", deliverables=["Full unit economics & inventory audit", "Supplier re-order schedule", "Q2 product line expansion plan"])
        ]
    },
    VentureArchetype.DEEPTECH_HARDWARE: {
        "messaging_framework": {
            "headline": "Pioneering Next-Generation Technology for Industry Transformation",
            "subheadline": "Patented, breakthrough performance engineered for mission-critical applications.",
            "elevator_pitch": "A deep technology venture delivering order-of-magnitude improvements through scientific innovation.",
            "proof_points": "Patents pending, university lab validated, verified benchmark specifications.",
            "primary_cta": "Request Technical Whitepaper & Pilot Partnership"
        },
        "acquisition_tactics": [
            "Executive-level direct outreach to VP of R&D and Innovation at Fortune 500 targets",
            "Publishing peer-reviewed technical whitepapers and benchmark evaluation data",
            "Securing speaking slots and technology demonstrations at premier industry symposiums",
            "Government R&D and non-dilutive innovation grant applications (SBIR/Horizon)"
        ],
        "prioritized_next_actions": [
            "Draft 10-page peer-reviewed technical specification whitepaper",
            "Map top 25 enterprise innovation labs with immediate pilot needs",
            "Prepare working physical/simulated prototype video demonstration",
            "Apply for targeted non-dilutive innovation grant funding"
        ],
        "weekly_sprints": [
            WeeklySprintItem(week=1, month=1, focus="Technical Whitepaper & IP Summary", target_kpi="Whitepaper reviewed by 3 peer advisors", deliverables=["10-page technical whitepaper PDF", "Executive summary one-pager", "IP protection filing review"]),
            WeeklySprintItem(week=2, month=1, focus="Prototype Demonstration Assets", target_kpi="3-minute technical video recorded", deliverables=["Lab bench demonstration video", "Benchmark data sheet vs incumbent tech", "Interactive technical specs web page"]),
            WeeklySprintItem(week=3, month=1, focus="Enterprise Target Account Mapping", target_kpi="Top 50 enterprise innovation labs mapped", deliverables=["Account mapping matrix with key contacts", "Personalized pilot outreach deck", "Mutual NDA template"]),
            WeeklySprintItem(week=4, month=1, focus="Direct Executive Outreach Wave 1", target_kpi="10 exploratory introductory meetings", deliverables=["Cold email/LinkedIn outreach to VPs of R&D", "Introductory capability briefing deck", "Pilot qualification rubric"]),
            WeeklySprintItem(week=5, month=2, focus="Industry Symposium Presentation", target_kpi="Symposium paper accepted / presentation held", deliverables=["Symposium slide deck", "Conference networking list", "Technical booth collateral"]),
            WeeklySprintItem(week=6, month=2, focus="Pilot Proposal Formulation", target_kpi="3 formal pilot proposals requested", deliverables=["Standard Paid Pilot Agreement (MOU)", "Pilot success criteria matrix", "Implementation timeline roadmap"]),
            WeeklySprintItem(week=7, month=2, focus="Grant & Non-Dilutive Funding Submissions", target_kpi="1 major grant proposal submitted", deliverables=["Grant application packet", "Academic collaborator letters of support", "R&D budget justification"]),
            WeeklySprintItem(week=8, month=2, focus="Pilot Negotiation & Security Review", target_kpi="1st Paid Pilot Contract in legal review", deliverables=["Security and compliance questionnaire", "On-premise / hardware deployment checklist", "Escalation protocol"]),
            WeeklySprintItem(week=9, month=3, focus="Pilot Contract Execution & Kickoff", target_kpi="First paid enterprise pilot signed", deliverables=["Countersigned Pilot Agreement", "Kickoff presentation with enterprise team", "Milestone tracking dashboard"]),
            WeeklySprintItem(week=10, month=3, focus="Mid-Pilot Benchmark Validation", target_kpi="Pilot technical benchmarks met", deliverables=["Weekly engineering update report", "Mid-term review presentation", "Telemetry data log analysis"]),
            WeeklySprintItem(week=11, month=3, focus="Commercial Conversion Proposal", target_kpi="Commercial production contract drafted", deliverables=["Full-scale multi-year deployment proposal", "Volume pricing matrix", "SLA contract draft"]),
            WeeklySprintItem(week=12, month=3, focus="DeepTech Milestone & Investor Synthesis", target_kpi="Seed round lead investor term sheet", deliverables=["Pilot validation report for investors", "Series Seed / A data room assets", "18-month commercial manufacturing roadmap"])
        ]
    }
}


def get_fallback_plan(archetype: VentureArchetype) -> Dict:
    """Returns the curated template plan for the given archetype."""
    return ARCHETYPE_TEMPLATES.get(archetype, ARCHETYPE_TEMPLATES[VentureArchetype.B2B_SAAS])
