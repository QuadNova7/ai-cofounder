"""Marketing & GTM Prompt Templates.

Structured prompts for generating tailored positioning statements,
messaging matrices, acquisition tactics, and 12-week sprint roadmaps.
"""

SYSTEM_MARKETING_PROMPT = """You are an elite Startup CMO, Growth Architect, and Product Marketing Executive (alumnus of Y Combinator, Reforge, and top hyper-growth tech companies).
Your responsibility is to take upstream startup research (Idea Analysis, Competitor Landscape, Business Model Canvas, Revenue Parameters, and Founder Constraints) and produce an investor-grade, actionable Go-To-Market (GTM) strategy.

Core Tenets:
1. Grounded & Realistic: No vague corporate fluff. Write punchy, actionable directives tailored to the venture's specific archetype and founder skillset.
2. 12-Week Weekly Horizon: Deliver 12 sequenced weekly sprints covering the first 90 days of execution.
3. Concrete Deliverables & Measurable KPIs: Every week must have a clear focus, a quantifiable target KPI (e.g. '10 discovery calls booked', 'Top 5 on Product Hunt'), and 3 concrete deliverables.
4. Output Format: Return valid JSON adhering strictly to the requested schema.
"""


def build_marketing_user_prompt(
    archetype_name: str,
    idea_summary: str,
    target_segments: str,
    competitors: str,
    channels: str,
    pricing_model: str,
    budget: float,
    founder_skills: str,
    constraints: str
) -> str:
    """Builds the comprehensive user prompt for the marketing LLM invocation."""
    return f"""Please formulate the Go-To-Market strategy and 12-week launch roadmap for this new venture:

### Venture Profile
- Venture Archetype: {archetype_name}
- Refined Value Proposition: {idea_summary}
- Target Customer Segments: {target_segments}
- Competitor Landscape: {competitors}
- Pricing Strategy & Model: {pricing_model}
- Available Marketing Budget: ${budget:,.2f}
- Founder Skills & Resources: {founder_skills or 'General founder'}
- Constraints: {constraints or 'None specified'}

### Selected Priority Channels (Bullseye Inner Circle)
{channels}

### Instructions
Generate a comprehensive GTM plan containing:
1. "positioning_statement": Geoffrey Moore style positioning statement ('For [target users], who [problem], [Product] is a [category] that [benefit]. Unlike [competitors], our product [differentiator].')
2. "messaging_framework": Key-value dictionary containing:
   - "headline": Punchy 6-10 word customer-facing value hook
   - "subheadline": Supporting 1-2 sentence clarification
   - "elevator_pitch": 30-second conversational pitch for founders
   - "proof_points": Core trust markers, data claims, or technical advantages
   - "primary_cta": Exact call-to-action button copy (e.g. 'Start Free Trial', 'Book 15-Min Demo')
3. "acquisition_tactics": List of 4-6 specific growth tactics executing on the chosen priority channels.
4. "prioritized_next_actions": 4 tangible founder tasks for Day 1 through Day 14.
5. "weekly_sprints": Array of exactly 12 weekly sprint objects (week: 1..12, month: 1..3, focus, target_kpi, deliverables: [3 items]).

Respond ONLY with a valid JSON object matching these keys:
{{
  "positioning_statement": "...",
  "messaging_framework": {{
    "headline": "...",
    "subheadline": "...",
    "elevator_pitch": "...",
    "proof_points": "...",
    "primary_cta": "..."
  }},
  "acquisition_tactics": ["...", "..."],
  "prioritized_next_actions": ["...", "..."],
  "weekly_sprints": [
    {{
      "week": 1,
      "month": 1,
      "focus": "...",
      "target_kpi": "...",
      "deliverables": ["...", "...", "..."]
    }}
  ]
}}
"""
